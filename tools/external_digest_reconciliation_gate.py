from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
REPORT = DIST / 'external_digest_reconciliation_report.json'
TOOLS = ROOT / 'tools'
PYTHON = sys.executable
ENV = {'PYTHONPATH': str(ROOT / 'src'), 'PYTHONDONTWRITEBYTECODE': '1'}


def run_json(tool_name: str) -> dict[str, Any]:
    proc = subprocess.run(
        [PYTHON, str(TOOLS / tool_name)],
        cwd=ROOT,
        env={**ENV, **dict(**__import__('os').environ)},
        capture_output=True,
        text=True,
        check=True,
    )
    stdout = proc.stdout.strip()
    if not stdout:
        return {}
    return json.loads(stdout)


def digest_summary(block: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for case_name, case_data in block.get('cases', {}).items():
        out[case_name] = {
            'bundle_digest_primary': case_data.get('primary', {}).get('bundle_digest'),
            'bundle_digest_secondary': (case_data.get('independent') or case_data.get('node_second_line') or {}).get('bundle_digest'),
            'decision_class_primary': case_data.get('primary', {}).get('decision_class'),
            'decision_class_secondary': (case_data.get('independent') or case_data.get('node_second_line') or {}).get('decision_class'),
            'parity_ok': case_data.get('parity_ok', False),
        }
    return out


def main() -> int:
    independent = run_json('independent_second_implementation_parity.py')
    node = run_json('node_out_of_family_parity.py')
    overall_ok = bool(independent.get('overall_ok') and node.get('overall_ok'))
    reconciled = {
        'independent_second_implementation': digest_summary(independent),
        'node_out_of_family_second_line': digest_summary(node),
    }
    report = {
        'overall_ok': overall_ok,
        'independent_overall_ok': independent.get('overall_ok', False),
        'node_overall_ok': node.get('overall_ok', False),
        'reconciliation': reconciled,
    }
    DIST.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True), encoding='utf-8')
    print(json.dumps({'overall_ok': overall_ok, 'report': str(REPORT.relative_to(ROOT))}, indent=2))
    return 0 if overall_ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
