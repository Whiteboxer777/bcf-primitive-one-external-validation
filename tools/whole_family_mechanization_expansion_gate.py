#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from bcf_primitive.compiler import compile_bundle
from bcf_primitive.runtime import SealedBoundaryRunner, refuse_non_bypass
from bcf_primitive.common import load_json
from bcf_primitive_verifier.kernel_support import parse_profile, evaluate_profile
from bcf_primitive_verifier.strict_json import load_path_strict
from bcf_primitive_verifier.admission_normal_form import compile_admission_normal_form, evaluate_anf
from bcf_primitive_verifier.compiled_backend import compile_compiled_backend, evaluate_compiled_backend
from bcf_primitive_verifier.verifier import verify_bundle
from bcf_primitive_verifier.runtime import replay_verdict
from bcf_primitive_verifier.witness_certificate import WITNESS_CERTIFICATE_SCHEMA, strip_witness_certificate
from jsonschema import Draft202012Validator

EXAMPLES = ROOT / 'examples' / 'canonical'
OUT_R = ROOT / 'REPORTS' / 'whole_family_mechanization_expansion_report.json'
OUT_D = ROOT / 'dist' / 'whole_family_mechanization_expansion_report.json'


def _validate_witness(payload: dict[str, object]) -> dict[str, object]:
    cert = payload.get('witness_certificate')
    if not isinstance(cert, dict):
        return {'ok': False, 'reason': 'missing_witness_certificate'}
    validator = Draft202012Validator(WITNESS_CERTIFICATE_SCHEMA)
    errs = list(validator.iter_errors(cert))
    source = strip_witness_certificate(payload)
    from bcf_primitive_verifier.common import digest_data
    body = {k: v for k, v in cert.items() if k != 'certificate_digest'}
    return {
        'ok': not errs and cert.get('source_digest') == digest_data(source) and cert.get('certificate_digest') == digest_data(body),
        'schema_ok': not errs,
        'source_digest_ok': cert.get('source_digest') == digest_data(source),
        'certificate_digest_ok': cert.get('certificate_digest') == digest_data(body),
        'certificate_type': cert.get('certificate_type'),
        'source_verdict': cert.get('source_verdict'),
    }


def _load_report(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding='utf-8'))


def run_gate(project_root: str | Path = ROOT) -> dict[str, object]:
    project_root = Path(project_root)
    supporting = {
        'mechanized_kernel': _load_report('dist/mechanized_kernel_gate_report.json'),
        'admission_normal_form': _load_report('dist/admission_normal_form_gate_report.json'),
        'compiled_backend': _load_report('dist/compiled_backend_gate_report.json'),
        'witness_certificate': _load_report('dist/witness_certificate_gate_report.json'),
    }

    profiles = [
        EXAMPLES / 'invoice_profile.json',
        EXAMPLES / 'invoice_profile_stricter.json',
        EXAMPLES / 'invoice_profile_weaker.json',
    ]
    requests = [
        ('allow', load_path_strict(EXAMPLES / 'invoice_request_allow.json')),
        ('deny', load_path_strict(EXAMPLES / 'invoice_deny_request.json')),
    ]

    parity_rows = []
    parity_ok = True
    for profile_path in profiles:
        profile = parse_profile(load_path_strict(profile_path))
        anf = compile_admission_normal_form(profile)
        backend = compile_compiled_backend(profile)
        req_rows = []
        for req_name, req in requests:
            ref = evaluate_profile(profile, req).verdict
            ref_norm = 'ALLOW' if ref == 'ALLOW' else 'REFUSAL'
            anf_eval = evaluate_anf(anf, profile, req)
            cb_eval = evaluate_compiled_backend(backend, req)
            same = ref_norm == anf_eval['verdict'] == anf_eval['reference_verdict'] == cb_eval['verdict']
            parity_ok = parity_ok and same
            req_rows.append({
                'request_kind': req_name,
                'reference_verdict': ref_norm,
                'anf_verdict': anf_eval['verdict'],
                'compiled_backend_verdict': cb_eval['verdict'],
                'overall_ok': same,
            })
        parity_rows.append({'profile': str(profile_path.relative_to(project_root)), 'request_rows': req_rows, 'overall_ok': all(r['overall_ok'] for r in req_rows)})

    tmp_bundle = project_root / '.whole_family_mechanization_bundle_tmp'
    if tmp_bundle.exists():
        shutil.rmtree(tmp_bundle)
    compile_bundle(EXAMPLES / 'invoice_profile.json', tmp_bundle)

    verification = verify_bundle(tmp_bundle)
    runner = SealedBoundaryRunner(tmp_bundle)
    action = {'action_id': 'wfme-emit', 'kind': 'emit', 'payload': {}}
    allow_req = load_path_strict(EXAMPLES / 'invoice_request_allow.json')
    deny_req = load_path_strict(EXAMPLES / 'invoice_deny_request.json')
    permit = runner.execute(allow_req, action)
    refusal = runner.execute(deny_req, action)
    replay_allow = replay_verdict(tmp_bundle, allow_req)
    replay_refusal = replay_verdict(tmp_bundle, deny_req)
    no_bypass = refuse_non_bypass(tmp_bundle, allow_req, 'whole-family-mechanization-direct-entrypoint')

    witness_rows = {
        'verification': _validate_witness(verification),
        'permit': _validate_witness(permit),
        'refusal': _validate_witness(refusal),
        'replay_allow': _validate_witness(replay_allow),
        'replay_refusal': _validate_witness(replay_refusal),
        'no_bypass': _validate_witness(no_bypass),
    }
    witness_ok = all(v['ok'] for v in witness_rows.values())

    fail_closed_checks = {
        'runtime_deny_is_refusal': refusal.get('verdict') == 'REFUSAL',
        'replay_deny_is_refusal': replay_refusal.get('verdict') == 'REFUSAL',
        'allow_runtime_is_allow': permit.get('verdict') == 'ALLOW',
        'replay_allow_is_allow': replay_allow.get('verdict') == 'ALLOW',
        'no_bypass_refusal_code': no_bypass.get('refusal_code') == 'REFUSE_NON_BYPASS_VIOLATION',
    }
    fail_closed_ok = all(fail_closed_checks.values())

    # Broken bundle verification path
    broken = project_root / '.whole_family_mechanization_broken_bundle_tmp'
    if broken.exists():
        shutil.rmtree(broken)
    compile_bundle(EXAMPLES / 'invoice_profile.json', broken)
    (broken / 'COMPILED_BACKEND.json').unlink()
    broken_verification = verify_bundle(broken)
    broken_check = {
        'overall_ok_false': broken_verification.get('overall_ok') is False,
        'verification_result_not_verified': broken_verification.get('verification_result') == 'NOT_VERIFIED',
        'witness_ok': _validate_witness(broken_verification)['ok'],
        'refusal_code': broken_verification.get('refusal_code'),
        'expected_refusal': broken_verification.get('refusal_code') == 'REFUSE_REQUIRED_FILES_MISSING',
    }
    broken_ok = all(v for k, v in broken_check.items() if isinstance(v, bool))

    shutil.rmtree(tmp_bundle)
    shutil.rmtree(broken)

    supporting_ok = all(r.get('overall_ok') is True for r in supporting.values())
    overall_ok = supporting_ok and parity_ok and witness_ok and fail_closed_ok and broken_ok
    report = {
        'overall_ok': overall_ok,
        'gate_name': 'whole_family_mechanization_expansion_gate',
        'supporting_reports': {k: {'overall_ok': v.get('overall_ok')} for k, v in supporting.items()},
        'parity_rows': parity_rows,
        'witness_rows': witness_rows,
        'fail_closed_no_bypass_checks': fail_closed_checks,
        'broken_bundle_verification_check': broken_check,
        'truth_boundary': {
            'status_label': 'executable_witness_whole_family_mechanization_expansion',
            'what_is_verified': [
                'reference_to_anf_verdict parity on canonical kernel corpus',
                'anf_to_compiled_backend verdict parity on canonical kernel corpus',
                'witness-certificate structural soundness for verification/permit/refusal/replay/no-bypass outputs',
                'fail-closed and no-bypass preservation on the selected canonical boundary paths',
            ],
            'what_is_not_claimed': [
                'whole-family theorem-prover discharge',
                'complete object-model mechanization',
                'complete canonicalization-family mechanization',
                'full scalable backend correctness beyond current kernel corpus',
            ],
        },
    }
    text = json.dumps(report, indent=2) + '\n'
    OUT_R.write_text(text, encoding='utf-8')
    OUT_D.write_text(text, encoding='utf-8')
    return report


if __name__ == '__main__':
    report = run_gate(ROOT)
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report['overall_ok'] else 1)
