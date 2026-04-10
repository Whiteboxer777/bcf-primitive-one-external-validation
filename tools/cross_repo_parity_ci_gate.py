#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / 'CI' / 'CROSS_REPO_PARITY_CONTRACT.json'
OUT_REPORTS = ROOT / 'REPORTS' / 'cross_repo_parity_ci_gate_report.json'
OUT_DIST = ROOT / 'dist' / 'cross_repo_parity_ci_gate_report.json'
EXPORT_ROOT = ROOT / 'repo_exports' / 'node_second_line_repo'


def loadj(path: Path):
    return json.loads(path.read_text())


def write_report(report: dict) -> None:
    text = json.dumps(report, indent=2) + '\n'
    OUT_REPORTS.write_text(text)
    OUT_DIST.write_text(text)


def main() -> int:
    issues: list[str] = []
    if not CONTRACT.exists():
        issues.append('Missing CI/CROSS_REPO_PARITY_CONTRACT.json')
        report = {'overall_ok': False, 'issues': issues}
        write_report(report)
        print(json.dumps(report, indent=2))
        return 1

    contract = loadj(CONTRACT)
    workflow_status: dict[str, bool] = {}
    for rel in contract.get('required_workflows', []):
        p = ROOT / rel
        workflow_status[rel] = p.exists()
        if not p.exists():
            issues.append(f'Missing required workflow: {rel}')

    inputs: dict[str, dict] = {}
    for rel in contract.get('required_main_reports', []):
        p = ROOT / rel
        inputs[rel] = {'exists': p.exists()}
        if not p.exists():
            issues.append(f'Missing required main report: {rel}')
    for rel in contract.get('required_export_reports', []):
        p = EXPORT_ROOT / Path(rel)
        label = str(Path('repo_exports/node_second_line_repo') / rel)
        inputs[label] = {'exists': p.exists()}
        if not p.exists():
            issues.append(f'Missing required export report: {label}')

    checks: dict[str, bool] = {}
    if not issues:
        main_node = loadj(ROOT / 'REPORTS' / 'node_out_of_family_parity_report.json')
        main_sub = loadj(ROOT / 'REPORTS' / 'node_verification_subfamily_parity_report.json')
        repo_self = loadj(EXPORT_ROOT / 'reports' / 'node_self_check_report.json')
        repo_discharge = loadj(EXPORT_ROOT / 'reports' / 'node_theorem_discharge_report.json')
        checks = {
            'main_node_parity_ok': main_node.get('overall_ok') is True,
            'main_node_subfamily_ok': main_sub.get('overall_ok') is True,
            'repo_self_check_ok': repo_self.get('overall_ok') is True,
            'repo_discharge_ok': repo_discharge.get('overall_ok') is True,
            'primitive_identity_match': repo_self.get('verification', {}).get('primitive_identity') == 'BCF Primitive One',
        }
        for key in contract.get('required_checks', []):
            if checks.get(key) is not True:
                issues.append(f'Required cross-repo parity check failed: {key}')

    report = {
        'overall_ok': not issues,
        'contract': str(CONTRACT.relative_to(ROOT)),
        'contract_scope': contract.get('contract_scope', 'unspecified'),
        'truth_boundary': contract.get('truth_boundary', {}),
        'status_label': 'export_prepared_machine_gated_parity_readiness',
        'workflow_status': workflow_status,
        'inputs': inputs,
        'checks': checks,
        'issues': issues,
    }
    write_report(report)
    print(json.dumps(report, indent=2))
    return 0 if report['overall_ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
