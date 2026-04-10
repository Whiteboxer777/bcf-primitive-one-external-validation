#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path
import sys

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from bcf_primitive.compiler import compile_bundle
from bcf_primitive.runtime import SealedBoundaryRunner, refuse_non_bypass
from bcf_primitive_verifier.common import canonical_bytes, digest_data, load_json
from bcf_primitive_verifier.refusal import REFUSAL_SCHEMA, PERMIT_SCHEMA, VERIFICATION_RESULT_SCHEMA
from bcf_primitive_verifier.runtime import replay_verdict
from bcf_primitive_verifier.verifier import verify_bundle
from bcf_primitive_verifier.witness_certificate import WITNESS_CERTIFICATE_SCHEMA

OUT_R = ROOT / 'REPORTS/object_canonicalization_impossibility_saturation_report.json'
OUT_D = ROOT / 'dist/object_canonicalization_impossibility_saturation_report.json'
EX = ROOT / 'examples' / 'canonical'


def _validate(schema: dict[str, object], payload: dict[str, object]) -> dict[str, object]:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.path))
    return {
        'ok': not errors,
        'error_count': len(errors),
        'errors': [{'path': list(e.path), 'message': e.message} for e in errors],
    }


def _safe_execute(runner: SealedBoundaryRunner, request: object, action: object) -> dict[str, object]:
    try:
        return runner.execute(request, action)
    except RuntimeError as exc:
        msg = str(exc)
        if msg.endswith('request_too_large'):
            from bcf_primitive.refusal import make_refusal
            return make_refusal(code='REFUSE_REQUEST_OVERSIZE', layer='runtime', bundle_digest=runner.runtime.bundle_digest, request_digest=digest_data(request), action_digest=digest_data(action), refusal_reasons=['REFUSE_REQUEST_OVERSIZE'], details={'source': 'object_canonicalization_impossibility_saturation_gate'})
        if msg.endswith('schema_invalid'):
            from bcf_primitive.refusal import make_refusal
            return make_refusal(code='REFUSE_SCHEMA_INVALID', layer='runtime', bundle_digest=runner.runtime.bundle_digest, request_digest=digest_data(request), action_digest=digest_data(action), refusal_reasons=['REFUSE_SCHEMA_INVALID'], details={'source': 'object_canonicalization_impossibility_saturation_gate'})
        if msg.endswith('action_descriptor_invalid'):
            from bcf_primitive.refusal import make_refusal
            return make_refusal(code='REFUSE_ACTION_DESCRIPTOR_INVALID', layer='runtime', bundle_digest=runner.runtime.bundle_digest, request_digest=digest_data(request), action_digest=digest_data(action), refusal_reasons=['REFUSE_ACTION_DESCRIPTOR_INVALID'], details={'source': 'object_canonicalization_impossibility_saturation_gate'})
        raise


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        bundle = tmp / 'bundle'
        compile_bundle(EX / 'invoice_profile.json', bundle)
        runner = SealedBoundaryRunner(bundle)

        allow_request = load_json(EX / 'invoice_request_allow.json')
        deny_request = load_json(EX / 'invoice_deny_request.json')
        valid_action = {'action_id': 'oci-allow', 'kind': 'emit', 'payload': {}}

        verification = verify_bundle(bundle)
        permit = runner.execute(allow_request, valid_action)
        refusal = runner.execute(deny_request, {'action_id': 'oci-deny', 'kind': 'emit', 'payload': {}})
        replay_allow = replay_verdict(bundle, allow_request)
        replay_refusal = replay_verdict(bundle, deny_request)

        # object-model structural soundness + negative mutations
        verification_schema = _validate(VERIFICATION_RESULT_SCHEMA, verification)
        permit_schema = _validate(PERMIT_SCHEMA, permit)
        refusal_schema = _validate(REFUSAL_SCHEMA, refusal)
        replay_refusal_schema = _validate(REFUSAL_SCHEMA, replay_refusal)
        witness_checks = {
            'verification_witness': _validate(WITNESS_CERTIFICATE_SCHEMA, verification['witness_certificate']),
            'permit_witness': _validate(WITNESS_CERTIFICATE_SCHEMA, permit['witness_certificate']),
            'refusal_witness': _validate(WITNESS_CERTIFICATE_SCHEMA, refusal['witness_certificate']),
            'replay_allow_witness': _validate(WITNESS_CERTIFICATE_SCHEMA, replay_allow['witness_certificate']),
            'replay_refusal_witness': _validate(WITNESS_CERTIFICATE_SCHEMA, replay_refusal['witness_certificate']),
        }

        verification_negative = dict(verification)
        verification_negative.pop('verification_result', None)
        permit_negative = dict(permit)
        permit_negative.pop('permit_binding', None)
        refusal_negative = dict(refusal)
        refusal_negative.pop('refusal_code', None)
        object_model = {
            'overall_ok': all([
                verification_schema['ok'],
                permit_schema['ok'],
                refusal_schema['ok'],
                replay_refusal_schema['ok'],
                all(v['ok'] for v in witness_checks.values()),
                not _validate(VERIFICATION_RESULT_SCHEMA, verification_negative)['ok'],
                not _validate(PERMIT_SCHEMA, permit_negative)['ok'],
                not _validate(REFUSAL_SCHEMA, refusal_negative)['ok'],
            ]),
            'checks': {
                'verification_schema': verification_schema,
                'permit_schema': permit_schema,
                'refusal_schema': refusal_schema,
                'replay_refusal_schema': replay_refusal_schema,
                'witness_checks': witness_checks,
                'verification_negative_rejected': not _validate(VERIFICATION_RESULT_SCHEMA, verification_negative)['ok'],
                'permit_missing_binding_rejected': not _validate(PERMIT_SCHEMA, permit_negative)['ok'],
                'refusal_missing_code_rejected': not _validate(REFUSAL_SCHEMA, refusal_negative)['ok'],
            },
        }

        # canonicalization breadth
        croot = ROOT / 'corpus' / 'canonicalization'
        tfc = ROOT / 'corpus' / 'theorem_families' / 'canonicalization'
        req_a = load_json(croot / 'request_semantically_equal_a.json')
        req_b = load_json(croot / 'request_semantically_equal_b.json')
        req_d = load_json(croot / 'request_distinct.json')
        act_a = load_json(tfc / 'action_equal_a.json')
        act_b = load_json(tfc / 'action_equal_b.json')
        act_d = load_json(tfc / 'action_distinct.json')
        obj_a = load_json(tfc / 'object_equal_a.json')
        obj_b = load_json(tfc / 'object_equal_b.json')
        obj_d = load_json(tfc / 'object_distinct.json')
        canonicalization = {
            'overall_ok': (
                canonical_bytes(req_a) == canonical_bytes(req_b)
                and digest_data(req_a) == digest_data(req_b)
                and canonical_bytes(req_a) != canonical_bytes(req_d)
                and canonical_bytes(act_a) == canonical_bytes(act_b)
                and digest_data(act_a) == digest_data(act_b)
                and canonical_bytes(act_a) != canonical_bytes(act_d)
                and canonical_bytes(obj_a) == canonical_bytes(obj_b)
                and digest_data(obj_a) == digest_data(obj_b)
                and canonical_bytes(obj_a) != canonical_bytes(obj_d)
                and canonical_bytes(json.loads(canonical_bytes(obj_a).decode('utf-8'))) == canonical_bytes(obj_a)
            ),
            'checks': {
                'request_equal_pair': canonical_bytes(req_a) == canonical_bytes(req_b),
                'request_distinct_pair': canonical_bytes(req_a) != canonical_bytes(req_d),
                'action_equal_pair': canonical_bytes(act_a) == canonical_bytes(act_b),
                'action_distinct_pair': canonical_bytes(act_a) != canonical_bytes(act_d),
                'generic_object_equal_pair': canonical_bytes(obj_a) == canonical_bytes(obj_b),
                'generic_object_distinct_pair': canonical_bytes(obj_a) != canonical_bytes(obj_d),
                'generic_object_idempotence': canonical_bytes(json.loads(canonical_bytes(obj_a).decode('utf-8'))) == canonical_bytes(obj_a),
            },
        }

        # impossibility saturation
        broken_bundle = tmp / 'broken_bundle'
        compile_bundle(EX / 'invoice_profile.json', broken_bundle)
        (broken_bundle / 'TRUST_ROOTS.json').unlink()
        not_verified = replay_verdict(broken_bundle, allow_request)
        invalid_action = load_json(ROOT / 'corpus' / 'theorem_families' / 'impossibility' / 'invalid_action_descriptor.json')
        invalid_action_refusal = _safe_execute(runner, allow_request, invalid_action)
        no_bypass = refuse_non_bypass(bundle, allow_request, 'direct-runtime-eval')
        verdicts = {
            'runtime_allow': permit['verdict'],
            'runtime_refusal': refusal['verdict'],
            'replay_allow': replay_allow['verdict'],
            'replay_refusal': replay_refusal['verdict'],
            'not_verified_replay': not_verified['verdict'],
            'invalid_action': invalid_action_refusal['verdict'],
        }
        impossibility = {
            'overall_ok': (
                not_verified['verdict'] == 'REFUSAL'
                and refusal['permit'] is False
                and all(v in {'ALLOW', 'REFUSAL'} for v in verdicts.values())
                and no_bypass['refusal_code'] == 'REFUSE_NON_BYPASS_VIOLATION'
                and invalid_action_refusal['verdict'] == 'REFUSAL'
            ),
            'checks': {
                'no_allow_without_verification': not_verified['verdict'],
                'no_permit_on_refusal': refusal['permit'],
                'verdict_universe_samples': verdicts,
                'no_bypass_code': no_bypass['refusal_code'],
                'invalid_action_descriptor_refusal': invalid_action_refusal['verdict'],
            },
        }

        report = {
            'overall_ok': object_model['overall_ok'] and canonicalization['overall_ok'] and impossibility['overall_ok'],
            'gate_name': 'object_canonicalization_impossibility_saturation_gate',
            'status_label': 'executable_witness_strong_object_canonicalization_impossibility_saturation',
            'families': {
                'object_model': object_model,
                'canonicalization': canonicalization,
                'impossibility': impossibility,
            },
            'truth_boundary': 'stronger executable witness saturation for implemented object-model, canonicalization, and impossibility surfaces; not theorem-prover-grade whole-family closure',
        }
        text = json.dumps(report, indent=2) + '\n'
        OUT_R.write_text(text, encoding='utf-8')
        OUT_D.write_text(text, encoding='utf-8')
        print(text)
        return 0 if report['overall_ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
