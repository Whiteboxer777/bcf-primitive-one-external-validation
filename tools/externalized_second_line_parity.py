from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SRC = ROOT / 'src'
EXT_SRC = ROOT / 'externalized_second_line' / 'src'
for p in (SRC, EXT_SRC):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from bcf_primitive.compiler import compile_bundle
from bcf_primitive.runtime import SealedBoundaryRunner
from bcf_primitive_verifier.runtime import replay_verdict
from bcf_primitive_verifier.verifier import verify_bundle
from bcf_primitive_externalized.runtime import ExternalizedRunner, replay_verdict_externalized
from bcf_primitive_externalized.verifier import verify_bundle_externalized
from tools.schema_validation_harness import _validate
from tools.independent_second_implementation_parity import _normalize
from bcf_primitive_verifier.refusal import PERMIT_SCHEMA, REFUSAL_SCHEMA, VERIFICATION_RESULT_SCHEMA


def run_externalized_second_line_parity(project_root: str | Path, profile: str | Path) -> dict[str, object]:
    project_root = Path(project_root)
    profile = Path(profile)
    bundle = project_root / '.externalized_second_line_parity_bundle_tmp'
    if bundle.exists():
        shutil.rmtree(bundle)
    compile_bundle(profile, bundle)
    primary_verify = verify_bundle(bundle)
    external_verify = verify_bundle_externalized(bundle)
    primary_runner = SealedBoundaryRunner(bundle)
    external_runner = ExternalizedRunner(bundle)
    allow_request = json.loads((project_root / 'corpus' / 'equivalence' / 'allow_request.json').read_text(encoding='utf-8'))
    deny_request = json.loads((project_root / 'corpus' / 'equivalence' / 'deny_request.json').read_text(encoding='utf-8'))
    allow_action = {'action_id': 'externalized-allow', 'kind': 'emit', 'payload': {}}
    deny_action = {'action_id': 'externalized-deny', 'kind': 'emit', 'payload': {}}
    primary_allow = primary_runner.execute(allow_request, allow_action)
    external_allow = external_runner.execute(allow_request, allow_action)
    primary_deny = primary_runner.execute(deny_request, deny_action)
    external_deny = external_runner.execute(deny_request, deny_action)
    primary_replay_allow = replay_verdict(bundle, allow_request)
    external_replay_allow = replay_verdict_externalized(bundle, allow_request)
    primary_replay_deny = replay_verdict(bundle, deny_request)
    external_replay_deny = replay_verdict_externalized(bundle, deny_request)
    cases = {
        'verify': (primary_verify, external_verify, VERIFICATION_RESULT_SCHEMA),
        'allow_runtime': (primary_allow, external_allow, PERMIT_SCHEMA),
        'deny_runtime': (primary_deny, external_deny, REFUSAL_SCHEMA),
        'allow_replay': (primary_replay_allow, external_replay_allow, None),
        'deny_replay': (primary_replay_deny, external_replay_deny, REFUSAL_SCHEMA),
    }
    case_reports = {}
    overall_ok = True
    for name, (left_raw, right_raw, schema) in cases.items():
        left = _normalize(left_raw)
        right = _normalize(right_raw)
        schema_ok = True
        if schema is not None:
            schema_ok = _validate(schema, left_raw)['ok'] and _validate(schema, right_raw)['ok']
        parity_ok = (
            left['primitive_identity'] == right['primitive_identity'] == 'BCF Primitive One'
            and left['decision_class'] == right['decision_class']
            and left.get('bundle_digest') == right.get('bundle_digest')
            and left.get('request_digest') == right.get('request_digest')
            and left.get('refusal_code') == right.get('refusal_code')
            and left.get('refusal_class') == right.get('refusal_class')
            and left.get('authority_kind') == right.get('authority_kind')
            and schema_ok
        )
        overall_ok = overall_ok and parity_ok
        case_reports[name] = {'parity_ok': parity_ok, 'primary': left, 'externalized': right}
    shutil.rmtree(bundle)
    return {'overall_ok': overall_ok, 'target_name': 'primary_surface_vs_externalized_second_line', 'cases': case_reports}


if __name__ == '__main__':
    print(json.dumps(run_externalized_second_line_parity(ROOT, ROOT / 'examples' / 'canonical' / 'invoice_profile.json'), indent=2, sort_keys=True))
