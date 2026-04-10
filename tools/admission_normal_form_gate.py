
#!/usr/bin/env python3
from __future__ import annotations
import json
import tempfile
from pathlib import Path

from bcf_primitive.compiler import compile_bundle
from bcf_primitive_verifier.verifier import verify_bundle
from bcf_primitive_verifier.admission_normal_form import compile_admission_normal_form, evaluate_anf
from bcf_primitive_verifier.common import canonical_bytes, digest_data, load_json
from bcf_primitive_verifier.kernel_support import parse_profile
from bcf_primitive_verifier.strict_json import load_path_strict

ROOT = Path(__file__).resolve().parents[1]
OUT_R = ROOT / 'REPORTS' / 'admission_normal_form_gate_report.json'
OUT_D = ROOT / 'dist' / 'admission_normal_form_gate_report.json'
SCHEMA_PATH = ROOT / 'schemas' / 'admission_normal_form.schema.json'
EXAMPLES = ROOT / 'examples' / 'canonical'


def write(report: dict) -> None:
    text = json.dumps(report, indent=2) + "\n"
    OUT_R.write_text(text)
    OUT_D.write_text(text)
def main() -> int:
    issues = []
    details = {}
    schema_exists = SCHEMA_PATH.exists()
    if not schema_exists:
        issues.append('missing schemas/admission_normal_form.schema.json')
    profiles = [EXAMPLES / 'invoice_profile.json', EXAMPLES / 'invoice_profile_stricter.json', EXAMPLES / 'invoice_profile_weaker.json']
    requests = [
        load_path_strict(EXAMPLES / 'invoice_request_allow.json'),
        load_path_strict(EXAMPLES / 'invoice_deny_request.json'),
    ]
    profile_rows = []
    all_ok = True
    for p in profiles:
        profile = parse_profile(load_path_strict(p))
        anf1 = compile_admission_normal_form(profile).to_dict()
        anf2 = compile_admission_normal_form(profile).to_dict()
        det_ok = anf1 == anf2
        idem_ok = canonical_bytes(anf1) == canonical_bytes(json.loads(canonical_bytes(anf1).decode('utf-8')))
        req_results = []
        parity_ok = True
        for req in requests:
            ev = evaluate_anf(compile_admission_normal_form(profile), profile, req)
            req_results.append(ev)
            parity_ok = parity_ok and ev['equivalent_to_reference']
        profile_rows.append({'profile': str(p.relative_to(ROOT)), 'deterministic': det_ok, 'idempotent_bytes': idem_ok, 'request_results': req_results, 'overall_ok': det_ok and idem_ok and parity_ok})
        all_ok = all_ok and det_ok and idem_ok and parity_ok
    with tempfile.TemporaryDirectory() as td:
        bundle = Path(td) / 'bundle'
        compile_bundle(EXAMPLES / 'invoice_profile.json', bundle)
        verify = verify_bundle(bundle)
        emitted = load_json(bundle / 'ADMISSION_NORMAL_FORM.json')
        recomp = compile_admission_normal_form(parse_profile(load_json(bundle / 'PROFILE_SOURCE.json'))).to_dict()
        bundle_ok = emitted == recomp and verify.get('details', {}).get('compiler_products', {}).get('checks', {}).get('admission_normal_form') is True and (bundle / 'ADMISSION_NORMAL_FORM.schema.json').exists()
        details['bundle_product'] = {'overall_ok': bundle_ok, 'verify_overall_ok': verify['overall_ok'], 'compiler_emits_anf': (bundle / 'ADMISSION_NORMAL_FORM.json').exists(), 'compiler_emits_schema': (bundle / 'ADMISSION_NORMAL_FORM.schema.json').exists()}
        all_ok = all_ok and bundle_ok
    report = {'overall_ok': schema_exists and all_ok and not issues, 'gate_name': 'admission_normal_form_gate', 'schema_exists': schema_exists, 'profile_rows': profile_rows, 'details': details, 'issues': issues}
    write(report)
    print(json.dumps(report, indent=2))
    return 0 if report['overall_ok'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
