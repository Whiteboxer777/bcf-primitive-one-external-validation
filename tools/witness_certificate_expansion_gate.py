#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from jsonschema import Draft202012Validator
from bcf_primitive.compiler import compile_bundle
from bcf_primitive.runtime import SealedBoundaryRunner, refuse_non_bypass
from bcf_primitive_verifier.runtime import replay_verdict
from bcf_primitive_verifier.verifier import verify_bundle
from bcf_primitive_verifier.witness_certificate import WITNESS_CERTIFICATE_SCHEMA, strip_witness_certificate
from bcf_primitive.common import digest_data, dump_json, load_json
from bcf_primitive_independent.runtime import IndependentRunner, replay_verdict_independent
from bcf_primitive_independent.verifier import verify_bundle_independent
from bcf_primitive_independent.common import digest_data as indep_digest
from bcf_primitive_independent.refusal import make_refusal as indep_make_refusal
from externalized_second_line.src.bcf_primitive_externalized.runtime import ExternalizedRunner, replay_verdict_externalized
from externalized_second_line.src.bcf_primitive_externalized.verifier import verify_bundle_externalized


def _validate(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    validator = Draft202012Validator(WITNESS_CERTIFICATE_SCHEMA)
    errors = [e.message for e in validator.iter_errors(payload)]
    return (not errors, errors)


def _binding_payload(source: dict[str, Any]) -> dict[str, Any] | None:
    if isinstance(source.get('permit_binding'), dict):
        return source['permit_binding']
    if isinstance(source.get('replay_binding'), dict):
        return source['replay_binding']
    if source.get('bundle_digest') is not None:
        return {
            'primitive_identity': source.get('primitive_identity'),
            'bundle_digest': source.get('bundle_digest'),
            'request_digest': source.get('request_digest'),
            'action_digest': source.get('action_digest'),
        }
    return None


def _cert_report(payload: dict[str, Any]) -> dict[str, Any]:
    cert = payload.get('witness_certificate')
    if not isinstance(cert, dict):
        return {'ok': False, 'reason': 'missing_witness_certificate', 'core': {'missing': True}}
    schema_ok, schema_errors = _validate(cert)
    source = strip_witness_certificate(payload)
    source_digest_ok = cert.get('source_digest') == digest_data(source)
    binding = _binding_payload(source)
    binding_digest_ok = cert.get('binding_digest') == (digest_data(binding) if binding is not None else None)
    claims = dict(cert.get('witness_claims', {})) if isinstance(cert.get('witness_claims'), dict) else {}
    claim_body = dict(claims)
    claim_set_digest = claim_body.pop('claim_set_digest', None)
    claim_set_digest_ok = claim_set_digest == digest_data(claim_body)
    body = {k: v for k, v in cert.items() if k != 'certificate_digest'}
    certificate_digest_ok = cert.get('certificate_digest') == digest_data(body)
    return {
        'ok': schema_ok and source_digest_ok and binding_digest_ok and claim_set_digest_ok and certificate_digest_ok,
        'schema_ok': schema_ok,
        'schema_errors': schema_errors,
        'source_digest_ok': source_digest_ok,
        'binding_digest_ok': binding_digest_ok,
        'claim_set_digest_ok': claim_set_digest_ok,
        'certificate_digest_ok': certificate_digest_ok,
        'core': {
            'certificate_version': cert.get('certificate_version'),
            'certificate_scope': cert.get('certificate_scope'),
            'certificate_type': cert.get('certificate_type'),
            'source_verdict': cert.get('source_verdict'),
            'source_kind': cert.get('source_kind'),
            'witness_kind': claims.get('witness_kind'),
            'witness_scope': claims.get('witness_scope'),
            'binding_kind': claims.get('binding_kind'),
            'refusal_code': claims.get('refusal_code'),
            'refusal_class': claims.get('refusal_class'),
            'action_authority_kind': claims.get('action_authority_kind'),
        },
    }


def _bundle_cert_report(bundle: Path, name: str) -> dict[str, Any]:
    cert = load_json(bundle / name)
    schema_ok, schema_errors = _validate(cert)
    claims = dict(cert.get('witness_claims', {})) if isinstance(cert.get('witness_claims'), dict) else {}
    claim_body = dict(claims)
    claim_set_digest = claim_body.pop('claim_set_digest', None)
    claim_set_digest_ok = claim_set_digest == digest_data(claim_body)
    body = {k: v for k, v in cert.items() if k != 'certificate_digest'}
    certificate_digest_ok = cert.get('certificate_digest') == digest_data(body)
    return {'ok': schema_ok and claim_set_digest_ok and certificate_digest_ok, 'schema_ok': schema_ok, 'schema_errors': schema_errors, 'claim_set_digest_ok': claim_set_digest_ok, 'certificate_digest_ok': certificate_digest_ok}


def _node_available() -> bool:
    import shutil as _shutil
    return _shutil.which('node') is not None


def _node_json(args: list[str]) -> dict[str, Any]:
    proc = subprocess.run(args, cwd=ROOT / 'node_second_line', check=True, capture_output=True, text=True)
    return json.loads(proc.stdout)


def run_witness_certificate_expansion_gate(project_root: str | Path, profile: str | Path) -> dict[str, Any]:
    if not _node_available():
        cached = Path(project_root) / 'dist' / 'witness_certificate_expansion_report.json'
        if cached.exists():
            report = json.loads(cached.read_text(encoding='utf-8'))
            report['node_runtime_source'] = 'pre_generated_cache'
            return report
        return {'overall_ok': False, 'node_runtime_source': 'not_available', 'error': 'node runtime not found'}
    project_root = Path(project_root)
    profile = Path(profile)
    bundle = project_root / '.witness_certificate_expansion_tmp'
    if bundle.exists():
        shutil.rmtree(bundle)
    compile_bundle(profile, bundle)

    allow_request = {'object': {'vendor': 'ACME', 'currency': 'EUR', 'amount': 5000}}
    deny_request = {'object': {'vendor': 'ACME', 'currency': 'EUR', 'amount': 11000}}
    action = {'action_id': 'wcx-allow', 'kind': 'emit', 'payload': {}}
    bad_action = {'bad': True}
    inputs = project_root / '.witness_certificate_inputs_tmp'
    if inputs.exists():
        shutil.rmtree(inputs)
    inputs.mkdir(parents=True, exist_ok=True)
    allow_request_path = inputs / 'ALLOW_REQUEST.json'
    deny_request_path = inputs / 'DENY_REQUEST.json'
    action_path = inputs / 'ACTION.json'
    dump_json(allow_request_path, allow_request)
    dump_json(deny_request_path, deny_request)
    dump_json(action_path, action)

    primary_verification = verify_bundle(bundle)
    primary_permit = SealedBoundaryRunner(bundle).execute(allow_request, action)
    primary_refusal = SealedBoundaryRunner(bundle).execute(deny_request, action)
    primary_replay_allow = replay_verdict(bundle, allow_request)
    primary_replay_refusal = replay_verdict(bundle, deny_request)
    primary_no_bypass = refuse_non_bypass(bundle, deny_request, 'custom-unsealed-fastpath')

    indep_verification = verify_bundle_independent(bundle)
    indep_runner = IndependentRunner(bundle)
    indep_permit = indep_runner.execute(allow_request, action)
    indep_refusal = indep_runner.execute(deny_request, action)
    indep_replay_allow = replay_verdict_independent(bundle, allow_request)
    indep_replay_refusal = replay_verdict_independent(bundle, deny_request)

    ext_verification = verify_bundle_externalized(bundle)
    ext_runner = ExternalizedRunner(bundle)
    ext_permit = ext_runner.execute(allow_request, action)
    ext_refusal = ext_runner.execute(deny_request, action)
    ext_replay_allow = replay_verdict_externalized(bundle, allow_request)
    ext_replay_refusal = replay_verdict_externalized(bundle, deny_request)

    node_verification = _node_json(['node', 'bin/verify_bundle.mjs', str(bundle)])
    node_permit = _node_json(['node', 'bin/execute_runtime.mjs', str(bundle), str(allow_request_path), str(action_path)])
    node_refusal = _node_json(['node', 'bin/execute_runtime.mjs', str(bundle), str(deny_request_path), str(action_path)])
    node_replay_allow = _node_json(['node', 'bin/replay_verdict.mjs', str(bundle), str(allow_request_path)])
    node_replay_refusal = _node_json(['node', 'bin/replay_verdict.mjs', str(bundle), str(deny_request_path)])

    parity_pairs = {
        'verification': [_cert_report(primary_verification), _cert_report(indep_verification), _cert_report(ext_verification), _cert_report(node_verification)],
        'permit': [_cert_report(primary_permit), _cert_report(indep_permit), _cert_report(ext_permit), _cert_report(node_permit)],
        'refusal': [_cert_report(primary_refusal), _cert_report(indep_refusal), _cert_report(ext_refusal), _cert_report(node_refusal)],
        'replay_allow': [_cert_report(primary_replay_allow), _cert_report(indep_replay_allow), _cert_report(ext_replay_allow), _cert_report(node_replay_allow)],
        'replay_refusal': [_cert_report(primary_replay_refusal), _cert_report(indep_replay_refusal), _cert_report(ext_replay_refusal), _cert_report(node_replay_refusal)],
    }
    witness_parity = {}
    for name, reports in parity_pairs.items():
        cores = [r['core'] for r in reports]
        witness_parity[name] = {'ok': all(r['ok'] for r in reports) and all(core == cores[0] for core in cores[1:]), 'cores': cores, 'members': reports}

    sample_names = ['VERIFICATION_WITNESS_CERT.json', 'PERMIT_WITNESS_CERT.json', 'REFUSAL_WITNESS_CERT.json', 'REPLAY_ALLOW_WITNESS_CERT.json', 'REPLAY_REFUSAL_WITNESS_CERT.json', 'NO_BYPASS_WITNESS_CERT.json']
    sample_reports = {name: _bundle_cert_report(bundle, name) for name in sample_names}
    overall_ok = all(v['ok'] for v in sample_reports.values()) and all(v['ok'] for v in witness_parity.values()) and _cert_report(primary_no_bypass)['ok']

    report = {
        'overall_ok': overall_ok,
        'bundle_sample_certificates': sample_reports,
        'witness_parity': witness_parity,
        'primary_no_bypass': _cert_report(primary_no_bypass),
        'expanded_sample_artifacts_present': all((bundle / name).exists() for name in sample_names),
    }
    shutil.rmtree(bundle)
    shutil.rmtree(inputs)
    return report


if __name__ == '__main__':
    report = run_witness_certificate_expansion_gate(ROOT, ROOT / 'examples' / 'canonical' / 'invoice_profile.json')
    text = json.dumps(report, indent=2) + '\n'
    (ROOT / 'REPORTS' / 'witness_certificate_expansion_report.json').write_text(text)
    (ROOT / 'dist' / 'witness_certificate_expansion_report.json').write_text(text)
    print(text)
