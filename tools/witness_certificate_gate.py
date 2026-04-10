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

from jsonschema import Draft202012Validator
from bcf_primitive.compiler import compile_bundle
from bcf_primitive.runtime import SealedBoundaryRunner
from bcf_primitive_verifier.runtime import replay_verdict
from bcf_primitive_verifier.verifier import verify_bundle
from bcf_primitive_verifier.witness_certificate import WITNESS_CERTIFICATE_SCHEMA, strip_witness_certificate
from bcf_primitive.common import digest_data, load_json


def _validate(schema: dict[str, object], payload: dict[str, object]) -> bool:
    validator = Draft202012Validator(schema)
    return not list(validator.iter_errors(payload))


def _check_output_certificate(payload: dict[str, object]) -> dict[str, object]:
    cert = payload.get('witness_certificate')
    if not isinstance(cert, dict):
        return {'ok': False, 'reason': 'missing_witness_certificate'}
    schema_ok = _validate(WITNESS_CERTIFICATE_SCHEMA, cert)
    source_digest_ok = cert.get('source_digest') == digest_data(strip_witness_certificate(payload))
    body = {k: v for k, v in cert.items() if k != 'certificate_digest'}
    certificate_digest_ok = cert.get('certificate_digest') == digest_data(body)
    return {
        'ok': schema_ok and source_digest_ok and certificate_digest_ok,
        'schema_ok': schema_ok,
        'source_digest_ok': source_digest_ok,
        'certificate_digest_ok': certificate_digest_ok,
    }


def _check_bundle_certificate(cert: dict[str, object]) -> dict[str, object]:
    schema_ok = _validate(WITNESS_CERTIFICATE_SCHEMA, cert)
    body = {k: v for k, v in cert.items() if k != 'certificate_digest'}
    certificate_digest_ok = cert.get('certificate_digest') == digest_data(body)
    return {'ok': schema_ok and certificate_digest_ok, 'schema_ok': schema_ok, 'certificate_digest_ok': certificate_digest_ok}


def run_witness_certificate_gate(project_root: str | Path, profile: str | Path) -> dict[str, object]:
    project_root = Path(project_root)
    profile = Path(profile)
    bundle = project_root / '.witness_certificate_bundle_tmp'
    if bundle.exists():
        shutil.rmtree(bundle)
    compile_bundle(profile, bundle)
    runner = SealedBoundaryRunner(bundle)
    allow_request = {'object': {'vendor': 'ACME', 'currency': 'EUR', 'amount': 5000}}
    deny_request = {'object': {'vendor': 'ACME', 'currency': 'EUR', 'amount': 11000}}

    verification = verify_bundle(bundle)
    permit = runner.execute(allow_request, {'action_id': 'wc-allow', 'kind': 'emit', 'payload': {}})
    refusal = runner.execute(deny_request, {'action_id': 'wc-deny', 'kind': 'emit', 'payload': {}})
    replay_refusal = replay_verdict(bundle, deny_request)

    report = {
        'verification': _check_output_certificate(verification),
        'permit': _check_output_certificate(permit),
        'refusal': _check_output_certificate(refusal),
        'replay_refusal': _check_output_certificate(replay_refusal),
        'sample_bundle_certificates': {
            'VERIFICATION_WITNESS_CERT.json': _check_bundle_certificate(load_json(bundle / 'VERIFICATION_WITNESS_CERT.json')),
            'PERMIT_WITNESS_CERT.json': _check_bundle_certificate(load_json(bundle / 'PERMIT_WITNESS_CERT.json')),
            'REFUSAL_WITNESS_CERT.json': _check_bundle_certificate(load_json(bundle / 'REFUSAL_WITNESS_CERT.json')),
        },
        'schema_artifact_present': (bundle / 'WITNESS_CERTIFICATE.schema.json').exists(),
    }
    report['overall_ok'] = (
        report['verification']['ok']
        and report['permit']['ok']
        and report['refusal']['ok']
        and report['replay_refusal']['ok']
        and report['schema_artifact_present']
        and all(v['ok'] for v in report['sample_bundle_certificates'].values())
    )
    shutil.rmtree(bundle)
    return report


if __name__ == '__main__':
    report = run_witness_certificate_gate(ROOT, ROOT / 'examples' / 'canonical' / 'invoice_profile.json')
    text = json.dumps(report, indent=2) + '\n'
    (ROOT / 'REPORTS' / 'witness_certificate_gate_report.json').write_text(text)
    (ROOT / 'dist' / 'witness_certificate_gate_report.json').write_text(text)
    print(text)
