from __future__ import annotations

import json
import shutil
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from bcf_primitive.compiler import compile_bundle
from bcf_primitive.runtime import SealedBoundaryRunner
from bcf_primitive_verifier.runtime import replay_verdict
from bcf_primitive_verifier.verifier import verify_bundle
from bcf_primitive_independent.runtime import IndependentRunner, replay_verdict_independent
from bcf_primitive_independent.verifier import verify_bundle_independent
from bcf_primitive_verifier.refusal import PRIMITIVE_IDENTITY
from tools.schema_validation_harness import _validate
from bcf_primitive_verifier.refusal import REFUSAL_SCHEMA, PERMIT_SCHEMA, VERIFICATION_RESULT_SCHEMA


def _normalize(payload: dict[str, object]) -> dict[str, object]:
    verdict = payload.get('verdict')
    if payload.get('verification_result') in {'VERIFIED', 'NOT_VERIFIED'}:
        return {
            'kind': 'verification',
            'primitive_identity': payload.get('primitive_identity'),
            'decision_class': payload.get('verification_result'),
            'bundle_digest': payload.get('bundle_digest'),
            'request_digest': None,
            'schema_ok': _validate(VERIFICATION_RESULT_SCHEMA, payload)['ok'],
            'refusal_code': payload.get('refusal_code'),
            'refusal_class': payload.get('refusal_class'),
            'authority_kind': None,
        }
    if verdict == 'ALLOW' and payload.get('permit') is True:
        return {
            'kind': 'permit',
            'primitive_identity': payload.get('primitive_identity'),
            'decision_class': 'ALLOW',
            'bundle_digest': payload.get('bundle_digest'),
            'request_digest': payload.get('request_digest'),
            'schema_ok': _validate(PERMIT_SCHEMA, payload)['ok'],
            'authority_kind': payload.get('action_authority', {}).get('kind'),
            'refusal_code': None,
            'refusal_class': None,
        }
    if verdict == 'ALLOW':
        return {
            'kind': 'replay_allow',
            'primitive_identity': payload.get('primitive_identity'),
            'decision_class': 'ALLOW',
            'bundle_digest': payload.get('bundle_digest'),
            'request_digest': payload.get('request_digest'),
            'schema_ok': True,
            'authority_kind': None,
            'refusal_code': None,
            'refusal_class': None,
        }
    return {
        'kind': 'refusal',
        'primitive_identity': payload.get('primitive_identity'),
        'decision_class': 'REFUSAL',
        'bundle_digest': payload.get('bundle_digest'),
        'request_digest': payload.get('request_digest'),
        'schema_ok': _validate(REFUSAL_SCHEMA, payload)['ok'],
        'refusal_code': payload.get('refusal_code'),
        'refusal_class': payload.get('refusal_class'),
        'authority_kind': None,
    }


def run_independent_second_implementation_parity(project_root: str | Path, profile: str | Path) -> dict[str, object]:
    project_root = Path(project_root)
    profile = Path(profile)
    bundle = project_root / '.independent_parity_bundle_tmp'
    if bundle.exists():
        shutil.rmtree(bundle)
    compile_bundle(profile, bundle)

    primary_verify = verify_bundle(bundle)
    independent_verify = verify_bundle_independent(bundle)

    primary_runner = SealedBoundaryRunner(bundle)
    independent_runner = IndependentRunner(bundle)

    allow_request = json.loads((project_root / 'corpus' / 'equivalence' / 'allow_request.json').read_text(encoding='utf-8'))
    deny_request = json.loads((project_root / 'corpus' / 'equivalence' / 'deny_request.json').read_text(encoding='utf-8'))

    action_allow = {'action_id': 'independent-allow', 'kind': 'emit', 'payload': {}}
    action_deny = {'action_id': 'independent-deny', 'kind': 'emit', 'payload': {}}

    primary_allow = primary_runner.execute(allow_request, action_allow)
    independent_allow = independent_runner.execute(allow_request, action_allow)
    primary_deny = primary_runner.execute(deny_request, action_deny)
    independent_deny = independent_runner.execute(deny_request, action_deny)
    primary_replay_allow = replay_verdict(bundle, allow_request)
    independent_replay_allow = replay_verdict_independent(bundle, allow_request)
    primary_replay_deny = replay_verdict(bundle, deny_request)
    independent_replay_deny = replay_verdict_independent(bundle, deny_request)

    cases = {
        'verify': (_normalize(primary_verify), _normalize(independent_verify)),
        'allow_runtime': (_normalize(primary_allow), _normalize(independent_allow)),
        'deny_runtime': (_normalize(primary_deny), _normalize(independent_deny)),
        'allow_replay': (_normalize(primary_replay_allow), _normalize(independent_replay_allow)),
        'deny_replay': (_normalize(primary_replay_deny), _normalize(independent_replay_deny)),
    }
    case_reports: dict[str, object] = {}
    overall_ok = True
    for name, (left, right) in cases.items():
        parity_ok = (
            left['primitive_identity'] == right['primitive_identity'] == PRIMITIVE_IDENTITY
            and left['decision_class'] == right['decision_class']
            and left.get('bundle_digest') == right.get('bundle_digest')
            and left.get('request_digest') == right.get('request_digest')
            and left['schema_ok'] is True
            and right['schema_ok'] is True
            and left.get('refusal_code') == right.get('refusal_code')
            and left.get('refusal_class') == right.get('refusal_class')
            and left.get('authority_kind') == right.get('authority_kind')
        )
        overall_ok = overall_ok and parity_ok
        case_reports[name] = {'parity_ok': parity_ok, 'primary': left, 'independent': right}

    report = {
        'overall_ok': overall_ok,
        'target_name': 'primary_surface_vs_independent_second_implementation',
        'cases': case_reports,
    }
    shutil.rmtree(bundle)
    return report


if __name__ == '__main__':
    print(json.dumps(run_independent_second_implementation_parity(ROOT, ROOT / 'examples' / 'canonical' / 'invoice_profile.json'), indent=2, sort_keys=True))
