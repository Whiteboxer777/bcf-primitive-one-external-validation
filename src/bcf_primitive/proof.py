from __future__ import annotations
import shutil, tempfile
from pathlib import Path
from .common import dump_json, load_json
from .compiler import compile_bundle
from .runtime import SealedBoundaryRunner, refuse_non_bypass
from .strict_json import load_path_strict
from .verifier import verify_bundle
def run_one_shot_proof(profile: str | Path, allow_request: str | Path, deny_request: str | Path) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix='bcf_primitive_proof_') as td:
        bundle = Path(td) / 'bundle'; compile_report = compile_bundle(profile, bundle); verify_report = verify_bundle(bundle); allow_req = load_path_strict(allow_request); deny_req = load_path_strict(deny_request); runner = SealedBoundaryRunner(bundle)
        allow_result = runner.execute(allow_req, {'action_id': 'a1', 'kind': 'emit', 'payload': {'ok': True}}); deny_result = runner.execute(deny_req, {'action_id': 'a2', 'kind': 'emit', 'payload': {'ok': False}})
        bad_bundle = Path(td) / 'tampered'; shutil.copytree(bundle, bad_bundle); (bad_bundle / 'CLAIM.json').write_text('{"tampered": true}', encoding='utf-8'); tamper_verify = verify_bundle(bad_bundle)
        missing_bundle = Path(td) / 'missing'; shutil.copytree(bundle, missing_bundle); (missing_bundle / 'AUTHORITY_POLICY.json').unlink(); missing_verify = verify_bundle(missing_bundle)
        mismatch_bundle = Path(td) / 'mismatch'; shutil.copytree(bundle, mismatch_bundle); contract = load_json(mismatch_bundle / 'BUNDLE_CONTRACT.json'); contract['contract_version'] = 'MISMATCHED'; dump_json(mismatch_bundle / 'BUNDLE_CONTRACT.json', contract); mismatch_verify = verify_bundle(mismatch_bundle)
        non_bypass = refuse_non_bypass(bundle, allow_req, 'direct-runtime-eval')
        return {'proof_ok': bool(compile_report['overall_ok'] and verify_report['overall_ok'] and allow_result['permit'] and (not deny_result['permit']) and ('REFUSE_MANIFEST_MISMATCH' in tamper_verify.get('refusal_reasons', [])) and ('REFUSE_REQUIRED_FILES_MISSING' in missing_verify.get('refusal_reasons', [])) and ('REFUSE_CONTRACT_MISMATCH' in mismatch_verify.get('refusal_reasons', [])) and (non_bypass['refusal_code'] == 'REFUSE_NON_BYPASS_VIOLATION')), 'compile_report': compile_report, 'verify_report': verify_report, 'allow_result': allow_result, 'deny_result': deny_result, 'tamper_verify': tamper_verify, 'missing_verify': missing_verify, 'mismatch_verify': mismatch_verify, 'non_bypass_refusal': non_bypass}
