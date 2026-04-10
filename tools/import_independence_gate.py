from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
PACKAGES = {
    'bcf_trust_kernel': {'allowed_internal': {'bcf_trust_kernel'}},
    'bcf_primitive': {'allowed_internal': {'bcf_trust_kernel', 'bcf_primitive', 'bcf_primitive_verifier'}},
    'bcf_primitive_verifier': {'allowed_internal': {'bcf_trust_kernel', 'bcf_primitive_verifier'}},
    'bcf_primitive_independent': {'allowed_internal': {'bcf_trust_kernel', 'bcf_primitive_independent'}},
}
PACKAGE_PREFIXES = tuple(PACKAGES)
OUT = ROOT / 'dist' / 'import_independence_report.json'


def _top_package(name: str) -> str | None:
    for pkg in PACKAGE_PREFIXES:
        if name == pkg or name.startswith(pkg + '.'):
            return pkg
    return None


def _imports_for(path: Path) -> list[dict[str, Any]]:
    tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    rows: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                rows.append({'kind': 'import', 'module': alias.name, 'line': node.lineno})
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            rows.append({'kind': 'from', 'module': module, 'level': node.level, 'line': node.lineno})
    return rows


def main() -> int:
    violations: list[dict[str, Any]] = []
    package_reports: dict[str, Any] = {}
    for pkg, cfg in PACKAGES.items():
        pkg_dir = SRC / pkg
        imports_report = []
        for path in sorted(pkg_dir.glob('*.py')):
            local = []
            for row in _imports_for(path):
                module = row['module']
                if row.get('level', 0) > 0:
                    local.append({**row, 'status': 'relative-local'})
                    continue
                top = _top_package(module)
                if top is None:
                    local.append({**row, 'status': 'external-or-stdlib'})
                    continue
                allowed = top in cfg['allowed_internal']
                entry = {**row, 'status': 'allowed' if allowed else 'forbidden', 'target_top_package': top}
                local.append(entry)
                if not allowed:
                    violations.append({'package': pkg, 'file': str(path.relative_to(ROOT)), **entry})
            imports_report.append({'file': str(path.relative_to(ROOT)), 'imports': local})
        package_reports[pkg] = {
            'allowed_internal': sorted(cfg['allowed_internal']),
            'files_checked': len(imports_report),
            'imports': imports_report,
        }
    report = {
        'pass_id': 'INDEPENDENCE_CLOSURE_AND_TRUST_COMPRESSION_PASS',
        'overall_ok': not violations,
        'forbidden_import_count': len(violations),
        'violations': violations,
        'packages': package_reports,
        'policy': {
            'bcf_trust_kernel': 'frozen minimal shared kernel only',
            'bcf_primitive': 'may import trust kernel and the official verifier facade, but not the independent package',
            'bcf_primitive_verifier': 'may import trust kernel, but not primary or independent package',
            'bcf_primitive_independent': 'must remain clean-room relative to primary/verifier families; trust-kernel sharing is explicitly declared and audited',
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, sort_keys=True), encoding='utf-8')
    print(json.dumps({'overall_ok': report['overall_ok'], 'forbidden_import_count': report['forbidden_import_count'], 'report': str(OUT.relative_to(ROOT))}, indent=2))
    return 0 if report['overall_ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
