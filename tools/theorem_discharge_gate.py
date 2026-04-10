#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / 'PROOFS' / 'THEOREM_DISCHARGE_LEDGER.md'
JSON_PATH = ROOT / 'PROOFS' / 'THEOREM_DISCHARGE_LEDGER.json'
POLICY_PATH = ROOT / 'SPEC' / 'THEOREM_DISCHARGE_POLICY.json'
OUT_REPORTS = ROOT / 'REPORTS' / 'theorem_discharge_gate_report.json'
OUT_DIST = ROOT / 'dist' / 'theorem_discharge_gate_report.json'


def write_report(report: dict) -> None:
    text = json.dumps(report, indent=2) + "\n"
    OUT_REPORTS.write_text(text)
    OUT_DIST.write_text(text)


def main() -> int:
    issues: list[str] = []
    warnings: list[str] = []
    for p in [MD_PATH, JSON_PATH, POLICY_PATH]:
        if not p.exists():
            issues.append(f'Missing {p.relative_to(ROOT)}')
    if issues:
        report = {'overall_ok': False, 'issues': issues, 'warnings': warnings}
        write_report(report)
        print(json.dumps(report, indent=2))
        return 1

    data = json.loads(JSON_PATH.read_text())
    policy = json.loads(POLICY_PATH.read_text())
    families = data.get('families', {})
    statuses = set(policy['closed_status_vocabulary'])
    theorem_families = policy.get('theorem_families', [])
    expected_statuses = policy.get('expected_family_statuses', {})

    if not families:
        issues.append('No theorem families present in JSON ledger.')

    for fam in theorem_families:
        if fam not in families:
            issues.append(f'Missing theorem family from ledger: {fam}')

    for fam, item in families.items():
        status = item.get('status')
        if status not in statuses:
            issues.append(f'{fam}: illegal status {status}')
        report_artifacts = item.get('report_artifacts', [])
        if not report_artifacts:
            issues.append(f'{fam}: missing report_artifacts')
        else:
            missing = [r for r in report_artifacts if not (ROOT / r).exists()]
            if missing:
                issues.append(f'{fam}: missing report_artifacts {missing}')
        witnesses = item.get('witnesses', {})
        if not witnesses:
            issues.append(f'{fam}: missing witness map')

    # Exact status truth sync
    for fam, expected in expected_statuses.items():
        actual = families.get(fam, {}).get('status')
        if actual != expected:
            issues.append(f'{fam}: exact theorem-discharge status drift ({actual} != {expected})')

    blocking = set(policy['release_blocking_families'])
    for fam in blocking:
        if fam not in families:
            issues.append(f'Release-blocking theorem family missing from ledger: {fam}')
        elif families[fam].get('status') != 'EXECUTABLE_WITNESS_STRONG':
            issues.append(f"{fam}: release-blocking family is not EXECUTABLE_WITNESS_STRONG ({families[fam].get('status')})")

    required_reports: dict[str, dict] = {}
    for rel in policy.get('required_reports', []):
        p = ROOT / rel
        ok = p.exists()
        required_reports[rel] = {'exists': ok}
        if not ok:
            issues.append(f'Required theorem-discharge report missing: {rel}')
            continue
        try:
            payload = json.loads(p.read_text())
            if 'overall_ok' in payload and payload['overall_ok'] is not True:
                issues.append(f'Required theorem-discharge report not ok: {rel}')
            required_reports[rel]['overall_ok'] = payload.get('overall_ok')
        except Exception as e:
            issues.append(f'Required theorem-discharge report unreadable: {rel}: {e}')

    report = {
        'overall_ok': not issues,
        'gate_name': 'theorem_discharge_gate',
        'markdown_ledger': str(MD_PATH.relative_to(ROOT)),
        'json_ledger': str(JSON_PATH.relative_to(ROOT)),
        'policy': str(POLICY_PATH.relative_to(ROOT)),
        'family_count': len(families),
        'exact_status_truth_sync': expected_statuses,
        'required_reports_checked': required_reports,
        'issues': issues,
        'warnings': warnings,
    }
    write_report(report)
    print(json.dumps(report, indent=2))
    return 0 if report['overall_ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
