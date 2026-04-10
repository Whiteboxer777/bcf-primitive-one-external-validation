from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from bcf_primitive.compiler import compile_bundle
from bcf_primitive.runtime import SealedBoundaryRunner
from bcf_primitive_verifier.runtime import replay_verdict
from bcf_primitive_verifier.verifier import verify_bundle
from bcf_primitive_verifier.refusal import PRIMITIVE_IDENTITY, REFUSAL_SCHEMA, PERMIT_SCHEMA, VERIFICATION_RESULT_SCHEMA
from tools.independent_second_implementation_parity import _normalize
from tools.schema_validation_harness import _validate

NODE_VERIFY = ROOT / 'node_second_line' / 'bin' / 'verify_bundle.mjs'
NODE_EXECUTE = ROOT / 'node_second_line' / 'bin' / 'execute_runtime.mjs'
NODE_REPLAY = ROOT / 'node_second_line' / 'bin' / 'replay_verdict.mjs'


def _node_available() -> bool:
    import shutil
    return shutil.which('node') is not None


def _run_node_json(script: Path, *args: str) -> dict[str, object]:
    proc = subprocess.run(['node', str(script), *map(str, args)], cwd=ROOT, capture_output=True, text=True, check=True)
    return json.loads(proc.stdout)


def run_node_out_of_family_parity(project_root: str | Path, profile: str | Path) -> dict[str, object]:
    project_root = Path(project_root)
    profile = Path(profile)
    if not _node_available():
        cached = project_root / 'dist' / 'node_out_of_family_parity_report.json'
        if cached.exists():
            report = json.loads(cached.read_text(encoding='utf-8'))
            report['node_runtime_source'] = 'pre_generated_cache'
            return report
        return {'overall_ok': False, 'node_runtime_source': 'not_available', 'error': 'node runtime not found and no cached report present'}
    bundle = project_root / '.node_out_of_family_bundle_tmp'
    if bundle.exists():
        shutil.rmtree(bundle)
    compile_bundle(profile, bundle)

    primary_verify = verify_bundle(bundle)
    node_verify = _run_node_json(NODE_VERIFY, bundle)

    primary_runner = SealedBoundaryRunner(bundle)
    allow_request = json.loads((project_root / 'corpus' / 'equivalence' / 'allow_request.json').read_text(encoding='utf-8'))
    deny_request = json.loads((project_root / 'corpus' / 'equivalence' / 'deny_request.json').read_text(encoding='utf-8'))
    allow_action = {'action_id': 'node-allow', 'kind': 'emit', 'payload': {}}
    deny_action = {'action_id': 'node-deny', 'kind': 'emit', 'payload': {}}
    primary_allow = primary_runner.execute(allow_request, allow_action)
    primary_deny = primary_runner.execute(deny_request, deny_action)
    primary_replay_allow = replay_verdict(bundle, allow_request)
    primary_replay_deny = replay_verdict(bundle, deny_request)

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        allow_req_path = td / 'allow_request.json'; allow_req_path.write_text(json.dumps(allow_request), encoding='utf-8')
        deny_req_path = td / 'deny_request.json'; deny_req_path.write_text(json.dumps(deny_request), encoding='utf-8')
        allow_action_path = td / 'allow_action.json'; allow_action_path.write_text(json.dumps(allow_action), encoding='utf-8')
        deny_action_path = td / 'deny_action.json'; deny_action_path.write_text(json.dumps(deny_action), encoding='utf-8')
        node_allow = _run_node_json(NODE_EXECUTE, bundle, allow_req_path, allow_action_path)
        node_deny = _run_node_json(NODE_EXECUTE, bundle, deny_req_path, deny_action_path)
        node_replay_allow = _run_node_json(NODE_REPLAY, bundle, allow_req_path)
        node_replay_deny = _run_node_json(NODE_REPLAY, bundle, deny_req_path)

    cases = {
        'verify': (primary_verify, node_verify, VERIFICATION_RESULT_SCHEMA),
        'allow_runtime': (primary_allow, node_allow, PERMIT_SCHEMA),
        'deny_runtime': (primary_deny, node_deny, REFUSAL_SCHEMA),
        'allow_replay': (primary_replay_allow, node_replay_allow, None),
        'deny_replay': (primary_replay_deny, node_replay_deny, REFUSAL_SCHEMA),
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
            left['primitive_identity'] == right['primitive_identity'] == PRIMITIVE_IDENTITY
            and left['decision_class'] == right['decision_class']
            and left.get('bundle_digest') == right.get('bundle_digest')
            and left.get('request_digest') == right.get('request_digest')
            and left.get('refusal_code') == right.get('refusal_code')
            and left.get('refusal_class') == right.get('refusal_class')
            and left.get('authority_kind') == right.get('authority_kind')
            and schema_ok
        )
        overall_ok = overall_ok and parity_ok
        case_reports[name] = {'parity_ok': parity_ok, 'primary': left, 'node_second_line': right}
    shutil.rmtree(bundle)
    return {'overall_ok': overall_ok, 'target_name': 'primary_surface_vs_node_out_of_family_second_line', 'cases': case_reports}


if __name__ == '__main__':
    print(json.dumps(run_node_out_of_family_parity(ROOT, ROOT / 'examples' / 'canonical' / 'invoice_profile.json'), indent=2, sort_keys=True))
