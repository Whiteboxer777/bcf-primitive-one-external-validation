#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / 'src') not in sys.path:
    sys.path.insert(0, str(ROOT / 'src'))

from bcf_primitive.compiler import compile_bundle
from bcf_primitive_verifier.admission_normal_form import compile_admission_normal_form, evaluate_anf
from bcf_primitive_verifier.compiled_backend import compile_compiled_backend, evaluate_compiled_backend
from bcf_primitive_verifier.common import canonical_bytes, load_json
from bcf_primitive_verifier.kernel_support import parse_profile
from bcf_primitive_verifier.strict_json import load_path_strict
from bcf_primitive_verifier.verifier import verify_bundle

OUT_R = ROOT / 'REPORTS' / 'compiled_backend_gate_report.json'
OUT_D = ROOT / 'dist' / 'compiled_backend_gate_report.json'
EXAMPLES = ROOT / 'examples' / 'canonical'
SCHEMA = ROOT / 'schemas' / 'compiled_backend.schema.json'


def write(report: dict) -> None:
    text = json.dumps(report, indent=2) + '\n'
    OUT_R.write_text(text)
    OUT_D.write_text(text)


def main() -> int:
    issues = []
    schema_exists = SCHEMA.exists()
    if not schema_exists:
        issues.append('missing schemas/compiled_backend.schema.json')

    profiles = [
        EXAMPLES / 'invoice_profile.json',
        EXAMPLES / 'invoice_profile_stricter.json',
        EXAMPLES / 'invoice_profile_weaker.json',
    ]
    requests = [
        load_path_strict(EXAMPLES / 'invoice_request_allow.json'),
        load_path_strict(EXAMPLES / 'invoice_deny_request.json'),
    ]

    profile_rows = []
    overall_ok = schema_exists and not issues
    for idx, profile_path in enumerate(profiles):
        profile = parse_profile(load_path_strict(profile_path))
        backend1 = compile_compiled_backend(profile).to_dict()
        backend2 = compile_compiled_backend(profile).to_dict()
        deterministic = backend1 == backend2
        idempotent_bytes = canonical_bytes(backend1) == canonical_bytes(json.loads(canonical_bytes(backend1).decode('utf-8')))
        anf = compile_admission_normal_form(profile)
        parity = True
        req_rows = []
        for req_idx, req in enumerate(requests):
            anf_eval = evaluate_anf(anf, profile, req)
            backend_eval = evaluate_compiled_backend(compile_compiled_backend(profile), req)
            same = backend_eval['verdict'] == anf_eval['verdict'] == anf_eval['reference_verdict']
            parity = parity and same
            req_rows.append({
                'request_kind': 'allow' if req_idx == 0 else 'deny',
                'compiled_verdict': backend_eval['verdict'],
                'anf_verdict': anf_eval['verdict'],
                'reference_verdict': anf_eval['reference_verdict'],
                'parity_ok': same,
            })
        ok = deterministic and idempotent_bytes and parity
        profile_rows.append({
            'profile': str(profile_path.relative_to(ROOT)),
            'deterministic': deterministic,
            'idempotent_bytes': idempotent_bytes,
            'request_rows': req_rows,
            'overall_ok': ok,
        })
        overall_ok = overall_ok and ok

    with tempfile.TemporaryDirectory() as td:
        bundle = Path(td) / 'bundle'
        compile_bundle(EXAMPLES / 'invoice_profile.json', bundle)
        verify = verify_bundle(bundle)
        emitted_backend = load_json(bundle / 'COMPILED_BACKEND.json')
        recomputed_backend = compile_compiled_backend(parse_profile(load_json(bundle / 'PROFILE_SOURCE.json'))).to_dict()
        bundle_ok = (
            emitted_backend == recomputed_backend
            and (bundle / 'COMPILED_BACKEND.schema.json').exists()
            and verify.get('details', {}).get('compiler_products', {}).get('checks', {}).get('compiled_backend') is True
            and verify.get('details', {}).get('compiled_backend_schema', {}).get('ok') is True
        )
        bundle_details = {
            'overall_ok': bundle_ok,
            'compiler_emits_compiled_backend': (bundle / 'COMPILED_BACKEND.json').exists(),
            'compiler_emits_compiled_backend_schema': (bundle / 'COMPILED_BACKEND.schema.json').exists(),
            'verification_compiled_backend_check': verify.get('details', {}).get('compiler_products', {}).get('checks', {}).get('compiled_backend'),
            'verification_compiled_backend_schema_check': verify.get('details', {}).get('compiled_backend_schema', {}).get('ok'),
        }
        overall_ok = overall_ok and bundle_ok

    report = {
        'overall_ok': overall_ok,
        'gate_name': 'compiled_backend_gate',
        'schema_exists': schema_exists,
        'profile_rows': profile_rows,
        'bundle_details': bundle_details,
        'issues': issues,
    }
    write(report)
    print(json.dumps(report, indent=2))
    return 0 if overall_ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
