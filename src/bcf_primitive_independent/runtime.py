from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from bcf_trust_kernel.witness_certificate import attach_witness_certificate

from .common import digest_data, load_json
from .semantic_core import parse_profile, evaluate_profile
from .refusal import make_permit, make_refusal
from .verifier import verify_bundle_independent


class IndependentRunner:
    def __init__(self, bundle_dir: str | Path):
        self.bundle = Path(bundle_dir)
        self.verification = verify_bundle_independent(self.bundle)
        self.manifest = load_json(self.bundle / 'MANIFEST.sha256.json')
        self.bundle_digest = digest_data(self.manifest)
        self.profile = parse_profile(load_json(self.bundle / 'PROFILE_SOURCE.json'))

    def _validate_request(self, request: Any) -> str | None:
        if not isinstance(request, dict):
            return 'REFUSE_SCHEMA_INVALID'
        encoded = json.dumps(request, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
        if len(encoded) > 64 * 1024:
            return 'REFUSE_REQUEST_OVERSIZE'
        if 'object' not in request or not isinstance(request['object'], dict):
            return 'REFUSE_SCHEMA_INVALID'
        return None

    def execute(self, request: dict[str, Any], action: dict[str, Any]) -> dict[str, Any]:
        request_digest = digest_data(request)
        if not self.verification.get('overall_ok', False):
            refusal = make_refusal(
                code=self.verification.get('refusal_code', 'REFUSE_BUNDLE_VERIFICATION_FAILED'),
                layer='bundle',
                bundle_digest=self.verification.get('bundle_digest'),
                request_digest=request_digest,
                verification_result='NOT_VERIFIED',
                refusal_reasons=self.verification.get('refusal_reasons', ['REFUSE_BUNDLE_VERIFICATION_FAILED']),
                details={'source': 'independent.execute'},
            )
            refusal['overall_ok'] = False
            return attach_witness_certificate(refusal)
        request_problem = self._validate_request(request)
        if request_problem is not None:
            refusal = make_refusal(code=request_problem, layer='runtime', bundle_digest=self.bundle_digest, request_digest=request_digest, refusal_reasons=[request_problem], details={'source': 'independent.execute'})
            refusal['overall_ok'] = False
            return attach_witness_certificate(refusal)
        if not isinstance(action, dict) or sorted(action.keys()) != ['action_id', 'kind', 'payload']:
            refusal = make_refusal(code='REFUSE_ACTION_DESCRIPTOR_INVALID', layer='action', bundle_digest=self.bundle_digest, request_digest=request_digest, action_digest=None, refusal_reasons=['REFUSE_ACTION_DESCRIPTOR_INVALID'], details={'source': 'independent.execute'})
            refusal['overall_ok'] = False
            return attach_witness_certificate(refusal)
        result = evaluate_profile(self.profile, request)
        if result.verdict != 'ALLOW':
            refusal = make_refusal(code='REFUSE_VERDICT_NOT_ALLOW', layer='action', bundle_digest=self.bundle_digest, request_digest=request_digest, action_digest=digest_data(action), refusal_reasons=['REFUSE_VERDICT_NOT_ALLOW'], details={'source': 'independent.execute', 'decisive_rule_ids': result.decisive_rule_ids, 'matched': result.matched, 'failed': result.failed, 'fail_closed': result.fail_closed})
            refusal['overall_ok'] = False
            return attach_witness_certificate(refusal)
        return attach_witness_certificate(make_permit(bundle_digest=self.bundle_digest, request_digest=request_digest, action=action, decisive_rule_ids=result.decisive_rule_ids))


def replay_verdict_independent(bundle_dir: str | Path, request: dict[str, Any]) -> dict[str, Any]:
    runner = IndependentRunner(bundle_dir)
    request_digest = digest_data(request)
    if not runner.verification.get('overall_ok', False):
        refusal = make_refusal(
            code=runner.verification.get('refusal_code', 'REFUSE_BUNDLE_VERIFICATION_FAILED'),
            layer='bundle',
            bundle_digest=runner.verification.get('bundle_digest'),
            request_digest=request_digest,
            verification_result='NOT_VERIFIED',
            refusal_reasons=runner.verification.get('refusal_reasons', ['REFUSE_BUNDLE_VERIFICATION_FAILED']),
            details={'source': 'independent.replay'},
        )
        refusal['overall_ok'] = False
        return attach_witness_certificate(refusal)
    request_problem = runner._validate_request(request)
    if request_problem is not None:
        refusal = make_refusal(code=request_problem, layer='runtime', bundle_digest=runner.bundle_digest, request_digest=request_digest, refusal_reasons=[request_problem], details={'source': 'independent.replay'})
        refusal['overall_ok'] = False
        return attach_witness_certificate(refusal)
    result = evaluate_profile(runner.profile, request)
    if result.verdict != 'ALLOW':
        refusal = make_refusal(code='REFUSE_VERDICT_NOT_ALLOW', layer='runtime', bundle_digest=runner.bundle_digest, request_digest=request_digest, refusal_reasons=['REFUSE_VERDICT_NOT_ALLOW'], details={'source': 'independent.replay', 'decisive_rule_ids': result.decisive_rule_ids, 'matched': result.matched, 'failed': result.failed, 'fail_closed': result.fail_closed})
        refusal['overall_ok'] = False
        return attach_witness_certificate(refusal)
    return attach_witness_certificate({
        'primitive_identity': 'BCF Primitive One',
        'overall_ok': True,
        'bundle_digest': runner.bundle_digest,
        'request_digest': request_digest,
        'verdict': 'ALLOW',
        'replay_binding': {'primitive_identity': 'BCF Primitive One', 'bundle_digest': runner.bundle_digest, 'request_digest': request_digest},
        'decisive_rule_ids': list(result.decisive_rule_ids),
        'matched': list(result.matched),
        'failed': list(result.failed),
        'fail_closed': result.fail_closed,
    })
