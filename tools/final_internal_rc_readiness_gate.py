#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_REPORTS = {
    'dist/adequacy_matrix_gate_report.json': ('overall_ok', True),
    'dist/theorem_discharge_gate_report.json': ('overall_ok', True),
    'dist/cross_repo_parity_ci_gate_report.json': ('overall_ok', True),
    'dist/mechanized_kernel_gate_report.json': ('overall_ok', True),
    'dist/equivalence_report.json': ('overall_ok', True),
    'dist/adversarial_closure_report.json': ('overall_ok', True),
    'dist/verification_subfamily_completion_report.json': ('overall_ok', True),
    'dist/compiled_backend_gate_report.json': ('overall_ok', True),
    'dist/witness_certificate_gate_report.json': ('overall_ok', True),
    'dist/witness_certificate_expansion_report.json': ('overall_ok', True),
    'dist/whole_family_mechanization_expansion_report.json': ('overall_ok', True),
    'dist/object_canonicalization_impossibility_saturation_report.json': ('overall_ok', True),
}

REQUIRED_DOCS = [
    'README.md',
    'SPEC/ADEQUACY_MATRIX.md',
    'SPEC/THEOREM_DISCHARGE_EXECUTABLE_CONTRACT.md',
    'SPEC/CROSS_REPO_PARITY_EXECUTABLE_CONTRACT.md',
    'PROOFS/MECHANIZED_KERNEL_SCOPE.md',
    'SPEC/COMPILED_BACKEND.md',
    'SPEC/COMPILED_BACKEND_EXECUTABLE_CONTRACT.md',
    'PROOFS/COMPILED_BACKEND_SCOPE.md',
    'SPEC/WITNESS_CERTIFICATES.md',
    'SPEC/WITNESS_CERTIFICATES_EXECUTABLE_CONTRACT.md',
    'PROOFS/WITNESS_CERTIFICATES_SCOPE.md',
    'SPEC/WITNESS_CERTIFICATE_EXPANSION.md',
    'SPEC/WITNESS_CERTIFICATE_EXPANSION_EXECUTABLE_CONTRACT.md',
    'PROOFS/WITNESS_CERTIFICATE_EXPANSION_SCOPE.md',
    'SPEC/WHOLE_FAMILY_MECHANIZATION_EXPANSION.md',
    'SPEC/WHOLE_FAMILY_MECHANIZATION_EXPANSION_EXECUTABLE_CONTRACT.md',
    'PROOFS/WHOLE_FAMILY_MECHANIZATION_EXPANSION_SCOPE.md',
    'SPEC/OBJECT_CANONICALIZATION_IMPOSSIBILITY_SATURATION.md',
    'SPEC/OBJECT_CANONICALIZATION_IMPOSSIBILITY_SATURATION_EXECUTABLE_CONTRACT.md',
    'PROOFS/OBJECT_CANONICALIZATION_IMPOSSIBILITY_SATURATION_SCOPE.md',
    'RC_CLAIM_BOUNDARY.md',
    'RC_RESIDUAL_GAPS.md',
]

RESIDUAL_GAPS = [
    {
        'gap_id': 'RG-04',
        'title': 'Fully external repo and CI execution',
        'status': 'OPEN',
        'exact_meaning': 'Cross-repo parity is export-prepared and machine-gated inside this artifact line, but not yet executed by an actually external hosted repository and independent CI governance boundary.'
    },
    {
        'gap_id': 'RG-05',
        'title': 'Whole-family mechanized theorem discharge',
        'status': 'OPEN',
        'exact_meaning': 'A real mechanized kernel plus ANF/compiled/witness expansion exists, but whole-family theorem-prover-grade discharge across the complete primitive family is not yet present.'
    },
]



def load_json(rel: str):
    p = ROOT / rel
    return json.loads(p.read_text(encoding='utf-8'))


def main():
    issues = []
    reports = {}
    for rel, (field, expected) in REQUIRED_REPORTS.items():
        p = ROOT / rel
        if not p.exists():
            issues.append(f'missing_report:{rel}')
            reports[rel] = {'exists': False}
            continue
        data = load_json(rel)
        reports[rel] = {'exists': True, field: data.get(field)}
        if data.get(field) != expected:
            issues.append(f'report_failed:{rel}:{field}={data.get(field)!r}')
    docs = {}
    for rel in REQUIRED_DOCS:
        exists = (ROOT / rel).exists()
        docs[rel] = exists
        if not exists:
            issues.append(f'missing_doc:{rel}')
    # Truth-boundary checks
    cross_repo = load_json('dist/cross_repo_parity_ci_gate_report.json')
    if cross_repo.get('status_label') != 'export_prepared_machine_gated_parity_readiness':
        issues.append('cross_repo_truth_label_drift')
    theorem_gate = load_json('dist/theorem_discharge_gate_report.json')
    status_map = theorem_gate.get('exact_status_truth_sync', {})
    if status_map.get('mechanized_kernel_preparation') != 'EXECUTABLE_WITNESS_STRONG':
        issues.append('mechanized_kernel_status_drift')
    if status_map.get('compiled_backend_preparation') != 'EXECUTABLE_WITNESS_STRONG':
        issues.append('compiled_backend_status_drift')
    if status_map.get('witness_certificate_preparation') != 'EXECUTABLE_WITNESS_STRONG':
        issues.append('witness_certificate_status_drift')
    if status_map.get('witness_certificate_expansion') != 'EXECUTABLE_WITNESS_STRONG':
        issues.append('witness_certificate_expansion_status_drift')
    if status_map.get('scope') != 'EXECUTABLE_WITNESS_PARTIAL':
        issues.append('theorem_family_truth_drift:scope')
    if status_map.get('closure') != 'EXECUTABLE_WITNESS_PARTIAL':
        issues.append('theorem_family_truth_drift:closure')
    for fam in ['object_model','canonicalization','impossibility','object_canonicalization_impossibility_saturation']:
        if status_map.get(fam) != 'EXECUTABLE_WITNESS_STRONG':
            issues.append(f'theorem_family_truth_drift:{fam}')
    adequacy = load_json('dist/adequacy_matrix_gate_report.json')
    if adequacy.get('counts', {}).get('gap_rows') is None:
        issues.append('adequacy_gap_rows_missing')

    report = {
        'overall_ok': not issues,
        'gate_name': 'final_internal_rc_readiness_gate',
        'required_reports': reports,
        'required_docs': docs,
        'truth_boundary_checks': {
            'cross_repo_status_label': cross_repo.get('status_label'),
            'theorem_status_truth_sync': status_map,
        },
        'residual_gaps': RESIDUAL_GAPS,
        'issues': issues,
    }
    out1 = ROOT / 'REPORTS/final_internal_rc_readiness_report.json'
    out2 = ROOT / 'dist/final_internal_rc_readiness_report.json'
    out1.write_text(json.dumps(report, indent=2), encoding='utf-8')
    out2.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
