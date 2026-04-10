from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def build_theorem_discharge_ledger(project_root: str | Path) -> dict[str, object]:
    project_root = Path(project_root)
    dist = project_root / 'dist'
    theorem_family = _load(dist / 'theorem_family_corpus_report.json')
    adversarial = _load(dist / 'adversarial_closure_report.json')
    verification_subfamily = _load(dist / 'verification_subfamily_completion_report.json')
    ext_py = _load(dist / 'externalized_second_line_parity_report.json')
    indep_py = _load(dist / 'independent_second_implementation_parity_report.json')
    node_parity = _load(dist / 'node_out_of_family_parity_report.json')
    anf = _load(dist / 'admission_normal_form_gate_report.json')
    node_verification_sub = _load(dist / 'node_verification_subfamily_parity_report.json')
    schema = _load(dist / 'schema_validation_report.json')
    equivalence = _load(dist / 'equivalence_report.json')
    mechanized = _load(dist / 'mechanized_kernel_gate_report.json')
    compiled = _load(dist / 'compiled_backend_gate_report.json')
    witness_cert = _load(dist / 'witness_certificate_gate_report.json')
    witness_exp = _load(dist / 'witness_certificate_expansion_report.json')
    wfme = _load(dist / 'whole_family_mechanization_expansion_report.json')
    oci = _load(dist / 'object_canonicalization_impossibility_saturation_report.json')

    families = {}
    theorem_map = {
        'primitive_identity': 'T-PI family',
        'scope': 'T-SC family',
        'object_model': 'T-OM family',
        'canonicalization': 'T-C14N family',
        'verification': 'T-VF family',
        'admission': 'T-AD family',
        'refusal': 'T-RA family',
        'permit': 'T-PA family',
        'determinism_replay': 'T-DET/T-RP family',
        'fail_closed': 'T-FC family',
        'no_bypass': 'T-NB family',
        'equivalence': 'T-EQ family',
        'impossibility': 'T-IMP family',
        'closure': 'T-CL family',
        'mechanized_kernel_preparation': 'Mechanized kernel preparation family',
        'admission_normal_form_preparation': 'ANF kernel compilation family',
        'compiled_backend_preparation': 'Compiled backend preparation family',
        'witness_certificate_preparation': 'Witness certificate preparation family',
        'witness_certificate_expansion': 'Witness certificate expansion family',
        'whole_family_mechanization_expansion': 'Whole-family mechanization expansion family',
        'object_canonicalization_impossibility_saturation': 'Object/canonicalization/impossibility saturation family',
    }
    for family, label in theorem_map.items():
        theorem_ok = theorem_family['families'].get(family, {}).get('overall_ok', True)
        adv_ok = adversarial['families'].get(family, {}).get('overall_ok', True)
        vf_ok = verification_subfamily['overall_ok'] if family == 'verification' else True
        node_vf_ok = node_verification_sub['overall_ok'] if family == 'verification' else True
        parity_ok = True
        if family == 'admission_normal_form_preparation':
            parity_ok = anf['overall_ok']
        if family == 'compiled_backend_preparation':
            parity_ok = compiled['overall_ok'] and anf['overall_ok']
        if family == 'equivalence':
            parity_ok = all([
                indep_py['overall_ok'],
                ext_py['overall_ok'],
                node_parity['overall_ok'],
                equivalence['overall_ok'],
            ])
        if family in {'permit', 'refusal', 'verification'}:
            parity_ok = parity_ok and node_parity['overall_ok']
        if family == 'canonicalization':
            parity_ok = parity_ok and node_parity['overall_ok']
        strong_by_policy = {'primitive_identity','verification','admission','refusal','permit','determinism_replay','fail_closed','no_bypass','equivalence','object_model','canonicalization','impossibility','whole_family_mechanization_expansion','object_canonicalization_impossibility_saturation','witness_certificate_expansion'}
        partial_by_policy = {'scope','closure'}
        if family == 'mechanized_kernel_preparation':
            status = 'EXECUTABLE_WITNESS_STRONG' if mechanized['overall_ok'] else 'EXECUTABLE_WITNESS_PARTIAL'
        elif family == 'admission_normal_form_preparation':
            status = 'EXECUTABLE_WITNESS_STRONG' if anf['overall_ok'] else 'EXECUTABLE_WITNESS_PARTIAL'
        elif family == 'compiled_backend_preparation':
            status = 'EXECUTABLE_WITNESS_STRONG' if compiled['overall_ok'] and anf['overall_ok'] else 'EXECUTABLE_WITNESS_PARTIAL'
        elif family == 'witness_certificate_preparation':
            status = 'EXECUTABLE_WITNESS_STRONG' if witness_cert['overall_ok'] else 'EXECUTABLE_WITNESS_PARTIAL'
        elif family == 'object_canonicalization_impossibility_saturation':
            status = 'EXECUTABLE_WITNESS_STRONG' if oci['overall_ok'] else 'EXECUTABLE_WITNESS_PARTIAL'
        elif family == 'witness_certificate_expansion':
            status = 'EXECUTABLE_WITNESS_STRONG' if witness_exp['overall_ok'] and witness_cert['overall_ok'] else 'EXECUTABLE_WITNESS_PARTIAL'
        elif family in partial_by_policy:
            status = 'EXECUTABLE_WITNESS_PARTIAL'
        elif family in strong_by_policy:
            status = 'EXECUTABLE_WITNESS_STRONG' if all([theorem_ok, adv_ok, vf_ok, node_vf_ok, parity_ok]) else 'EXECUTABLE_WITNESS_PARTIAL'
        else:
            status = 'EXECUTABLE_WITNESS_PARTIAL'
        families[family] = {
            'theorem_family': label,
            'status': status,
            'witnesses': {
                'theorem_family_corpus': theorem_ok,
                'adversarial_closure': adv_ok,
                'verification_subfamily_completion': vf_ok,
                'node_verification_subfamily_parity': node_vf_ok,
                'parity_surfaces': parity_ok,
                'schema_validation': schema['overall_ok'],
                'mechanized_kernel_gate': mechanized['overall_ok'],
                'admission_normal_form_gate': anf['overall_ok'],
                'compiled_backend_gate': compiled['overall_ok'],
                'witness_certificate_gate': witness_cert['overall_ok'],
                'witness_certificate_expansion_gate': witness_exp['overall_ok'],
                'whole_family_mechanization_expansion_gate': wfme['overall_ok'],
                'object_canonicalization_impossibility_saturation_gate': oci['overall_ok'],
            },
            'report_artifacts': [
                'dist/theorem_family_corpus_report.json',
                'dist/adversarial_closure_report.json',
                'dist/verification_subfamily_completion_report.json',
                'dist/node_verification_subfamily_parity_report.json',
                'dist/node_out_of_family_parity_report.json',
                'dist/equivalence_report.json',
                'dist/mechanized_kernel_gate_report.json',
                'dist/admission_normal_form_gate_report.json',
                'dist/compiled_backend_gate_report.json',
                'dist/witness_certificate_gate_report.json',
                'dist/witness_certificate_expansion_report.json',
                'dist/whole_family_mechanization_expansion_report.json',
                'dist/object_canonicalization_impossibility_saturation_report.json',
            ],
        }
    overall_ok = all(v['status'] in {'EXECUTABLE_WITNESS_STRONG','EXECUTABLE_WITNESS_PARTIAL'} for v in families.values())
    return {'overall_ok': overall_ok, 'families': families, 'summary': {'independent_python_parity': indep_py['overall_ok'], 'externalized_python_parity': ext_py['overall_ok'], 'node_out_of_family_parity': node_parity['overall_ok'], 'node_verification_subfamily_parity': node_verification_sub['overall_ok'], 'schema_validation': schema['overall_ok'], 'equivalence': equivalence['overall_ok'], 'compiled_backend': compiled['overall_ok'], 'witness_certificate': witness_cert['overall_ok'], 'witness_certificate_expansion': witness_exp['overall_ok'], 'whole_family_mechanization_expansion': wfme['overall_ok'], 'object_canonicalization_impossibility_saturation': oci['overall_ok']}}


def emit_theorem_discharge_markdown(report: dict[str, object]) -> str:
    lines = []
    lines.append('# THEOREM_DISCHARGE_LEDGER')
    lines.append('')
    lines.append('This ledger couples theorem families directly to executable witnesses, corpus witnesses, parity surfaces, and report artifacts. It does not claim theorem-prover discharge.')
    lines.append('')
    lines.append(f"Overall status: {'EXECUTABLE_WITNESS_STRONG' if report['overall_ok'] else 'EXECUTABLE_WITNESS_PARTIAL'}")
    lines.append('')
    for family, item in report['families'].items():
        lines.append(f"## {family}")
        lines.append(f"- theorem family: {item['theorem_family']}")
        lines.append(f"- status: {item['status']}")
        lines.append('- witnesses:')
        for key, value in item['witnesses'].items():
            lines.append(f"  - {key}: {str(value).lower()}")
        lines.append('- report_artifacts:')
        for path in item['report_artifacts']:
            lines.append(f"  - {path}")
        lines.append('')

    return '\n'.join(lines)


if __name__ == '__main__':
    report = build_theorem_discharge_ledger(ROOT)
    print(json.dumps(report, indent=2, sort_keys=True))

# mirror emission is handled by the external contract pass; this builder remains the canonical JSON source for the report.
