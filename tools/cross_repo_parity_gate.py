from __future__ import annotations
import json
from pathlib import Path

def loadj(p: Path):
    return json.loads(p.read_text())

def main() -> int:
    root = Path(__file__).resolve().parents[1]
    report = {
        'overall_ok': True,
        'inputs': {},
        'checks': {},
    }
    inputs = {
        'main_node_parity': root / 'REPORTS' / 'node_out_of_family_parity_report.json',
        'main_node_subfamily': root / 'REPORTS' / 'node_verification_subfamily_parity_report.json',
        'repo_local_discharge': root / 'repo_exports' / 'node_second_line_repo' / 'reports' / 'node_theorem_discharge_report.json',
        'repo_local_self_check': root / 'repo_exports' / 'node_second_line_repo' / 'reports' / 'node_self_check_report.json',
    }
    for k, p in inputs.items():
        report['inputs'][k] = {'path': str(p.relative_to(root)), 'exists': p.exists()}
        report['overall_ok'] = report['overall_ok'] and p.exists()
    if report['overall_ok']:
        main_node_parity = loadj(inputs['main_node_parity'])
        main_node_subfamily = loadj(inputs['main_node_subfamily'])
        repo_discharge = loadj(inputs['repo_local_discharge'])
        repo_self = loadj(inputs['repo_local_self_check'])
        report['checks'] = {
            'main_node_parity_ok': bool(main_node_parity.get('overall_ok') is True),
            'main_node_subfamily_ok': bool(main_node_subfamily.get('overall_ok') is True),
            'repo_discharge_ok': bool(repo_discharge.get('overall_ok') is True),
            'repo_self_check_ok': bool(repo_self.get('overall_ok') is True),
            'primitive_identity_match': repo_self.get('verification', {}).get('primitive_identity') == 'BCF Primitive One',
        }
        report['overall_ok'] = report['overall_ok'] and all(report['checks'].values())
    text = json.dumps(report, indent=2) + '\n'
    (root / 'REPORTS' / 'cross_repo_parity_gate_report.json').write_text(text)
    (root / 'dist' / 'cross_repo_parity_gate_report.json').write_text(text)
    print(text)
    return 0 if report['overall_ok'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
