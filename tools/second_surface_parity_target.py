from __future__ import annotations

import json
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
from bcf_primitive_verifier.refusal import PRIMITIVE_IDENTITY
from tools.schema_validation_harness import _validate
from bcf_primitive_verifier.refusal import REFUSAL_SCHEMA, PERMIT_SCHEMA


def _normalize_runtime(payload: dict[str, object]) -> dict[str, object]:
    if payload.get('verdict') == 'ALLOW':
        return {
            'surface': 'runtime_release_surface',
            'primitive_identity': payload.get('primitive_identity'),
            'decision_class': 'ALLOW',
            'bundle_digest': payload.get('bundle_digest'),
            'request_digest': payload.get('request_digest'),
            'schema_ok': _validate(PERMIT_SCHEMA, payload)['ok'],
            'authority_kind': payload.get('action_authority', {}).get('kind'),
        }
    return {
        'surface': 'runtime_release_surface',
        'primitive_identity': payload.get('primitive_identity'),
        'decision_class': 'REFUSAL',
        'bundle_digest': payload.get('bundle_digest'),
        'request_digest': payload.get('request_digest'),
        'schema_ok': _validate(REFUSAL_SCHEMA, payload)['ok'],
        'refusal_code': payload.get('refusal_code'),
        'refusal_class': payload.get('refusal_class'),
    }


def _normalize_replay(payload: dict[str, object]) -> dict[str, object]:
    verdict = payload.get('verdict')
    decision_class = 'ALLOW' if verdict == 'ALLOW' else 'REFUSAL'
    return {
        'surface': 'verifier_replay_surface',
        'primitive_identity': payload.get('primitive_identity', PRIMITIVE_IDENTITY),
        'decision_class': decision_class,
        'bundle_digest': payload.get('bundle_digest'),
        'request_digest': payload.get('request_digest'),
        'schema_ok': _validate(REFUSAL_SCHEMA, payload)['ok'] if decision_class == 'REFUSAL' else True,
        'refusal_code': payload.get('refusal_code') if decision_class == 'REFUSAL' else None,
    }


def run_second_surface_parity_target(project_root: str | Path, profile: str | Path) -> dict[str, object]:
    project_root = Path(project_root)
    profile = Path(profile)
    bundle = project_root / '.second_surface_bundle_tmp'
    if bundle.exists():
        import shutil
        shutil.rmtree(bundle)
    compile_bundle(profile, bundle)
    runner = SealedBoundaryRunner(bundle)

    corpus = project_root / 'corpus' / 'equivalence'
    cases = {
        'allow_case': json.loads((corpus / 'allow_request.json').read_text(encoding='utf-8')),
        'deny_case': json.loads((corpus / 'deny_request.json').read_text(encoding='utf-8')),
    }
    results: dict[str, object] = {}
    overall_ok = True
    for case_name, request in cases.items():
        runtime_payload = runner.execute(request, {'action_id': case_name, 'kind': 'emit', 'payload': {}})
        replay_payload = replay_verdict(bundle, request)
        runtime_norm = _normalize_runtime(runtime_payload)
        replay_norm = _normalize_replay(replay_payload)
        parity_ok = (
            runtime_norm['primitive_identity'] == replay_norm['primitive_identity'] == PRIMITIVE_IDENTITY
            and runtime_norm['bundle_digest'] == replay_norm['bundle_digest']
            and runtime_norm['request_digest'] == replay_norm['request_digest']
            and runtime_norm['decision_class'] == replay_norm['decision_class']
            and runtime_norm['schema_ok'] is True
            and replay_norm['schema_ok'] is True
        )
        overall_ok = overall_ok and parity_ok
        results[case_name] = {
            'parity_ok': parity_ok,
            'runtime_surface': runtime_norm,
            'verifier_surface': replay_norm,
        }
    report = {
        'overall_ok': overall_ok,
        'target_name': 'runtime_surface_vs_verifier_surface_parity',
        'cases': results,
    }
    import shutil
    shutil.rmtree(bundle)
    return report


if __name__ == '__main__':
    print(json.dumps(run_second_surface_parity_target(ROOT, ROOT / 'examples' / 'canonical' / 'invoice_profile.json'), indent=2, sort_keys=True))
