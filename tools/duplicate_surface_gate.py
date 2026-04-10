from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'dist' / 'duplicate_surface_gate_report.json'
PACKAGES = [
    ROOT / 'src' / 'bcf_trust_kernel',
    ROOT / 'src' / 'bcf_primitive',
    ROOT / 'src' / 'bcf_primitive_verifier',
    ROOT / 'src' / 'bcf_primitive_independent',
]
ALLOWED_DUPLICATE_BASENAMES = {
    '__init__.py',
    'common.py', 'contract.py', 'governance.py', 'strict_json.py', 'refusal.py', 'witness_certificate.py',
    'kernel_support.py', 'admission_normal_form.py', 'compiled_backend.py', 'verifier.py',
}
ALLOWED_FACADES = {
    'from bcf_trust_kernel.',
    'from bcf_primitive_verifier.verifier import *',
    'from .semantic_core import EvalResult, evaluate_profile as evaluate_request',
}

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def is_allowed_duplicate(path: Path) -> tuple[bool, str]:
    text = path.read_text(encoding='utf-8')
    if path.name in ALLOWED_DUPLICATE_BASENAMES and any(token in text for token in ALLOWED_FACADES):
        return True, 'authorized facade/shared-surface wrapper'
    if path.name == '__init__.py':
        return True, 'package initializer'
    return False, 'material duplicate semantic/code surface'

def main() -> int:
    files = [p for pkg in PACKAGES for p in pkg.glob('*.py')]
    by_hash: dict[str, list[Path]] = {}
    for path in files:
        by_hash.setdefault(sha(path), []).append(path)
    duplicate_groups = []
    violations = []
    for digest, group in sorted(by_hash.items()):
        if len(group) < 2:
            continue
        rels = [str(p.relative_to(ROOT)) for p in sorted(group)]
        statuses = []
        allowed = True
        for path in group:
            ok, reason = is_allowed_duplicate(path)
            statuses.append({'path': str(path.relative_to(ROOT)), 'allowed': ok, 'reason': reason})
            allowed = allowed and ok
        row = {'digest': digest, 'files': rels, 'allowed': allowed, 'statuses': statuses}
        duplicate_groups.append(row)
        if not allowed:
            violations.append(row)
    report = {
        'overall_ok': not violations,
        'duplicate_group_count': len(duplicate_groups),
        'violation_count': len(violations),
        'duplicate_groups': duplicate_groups,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True), encoding='utf-8')
    return 0 if report['overall_ok'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
