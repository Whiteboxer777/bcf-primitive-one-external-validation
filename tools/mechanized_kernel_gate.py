from __future__ import annotations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mechanized_kernel.checker import run_mechanized_kernel_check


def main() -> int:
    report = run_mechanized_kernel_check()
    report['contract_scope'] = 'mechanized_kernel_preparation_gate'
    report['truth_boundary'] = (
        'finite-state semantic kernel + canonicalization subset witness; '
        'not full theorem-prover discharge of the entire primitive family'
    )
    dist = ROOT / 'dist'
    reports = ROOT / 'REPORTS'
    dist.mkdir(exist_ok=True)
    reports.mkdir(exist_ok=True)
    for out in [dist / 'mechanized_kernel_gate_report.json', reports / 'mechanized_kernel_gate_report.json']:
        out.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    return 0 if report['overall_ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
