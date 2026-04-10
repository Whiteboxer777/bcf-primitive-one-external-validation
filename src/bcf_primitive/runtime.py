from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .common import digest_data, load_json
from .contract import bundle_contract
from .kernel_support import evaluate_profile, parse_profile
from .refusal import PRIMITIVE_IDENTITY, make_refusal
from .verifier import verify_bundle
from .witness_certificate import attach_witness_certificate

REFUSAL_CODES = {
    'bundle_verification_failed': 'REFUSE_BUNDLE_VERIFICATION_FAILED',
    'request_too_large': 'REFUSE_REQUEST_OVERSIZE',
    'schema_invalid': 'REFUSE_SCHEMA_INVALID',
    'action_descriptor_invalid': 'REFUSE_ACTION_DESCRIPTOR_INVALID',
    'verdict_not_allow': 'REFUSE_VERDICT_NOT_ALLOW',
    'non_bypass_violation': 'REFUSE_NON_BYPASS_VIOLATION',
}

class _InternalVerifiedRuntime:
    def __init__(self, bundle_dir: str | Path):
        self.bundle_dir = Path(bundle_dir)
        self.verification_report = verify_bundle(self.bundle_dir)
        if not self.verification_report.get('overall_ok', False):
            raise RuntimeError('runtime_refusal:bundle_verification_failed')
        self.profile = parse_profile(load_json(self.bundle_dir / 'PROFILE_SOURCE.json'))
        self.manifest = load_json(self.bundle_dir / bundle_contract.manifest_name)
        self.bundle_digest = digest_data(self.manifest)
        self.audit_log_path = self.bundle_dir / 'SEALED_RUNNER_AUDIT.jsonl'

    def validate_request(self, request: Any) -> None:
        if not isinstance(request, dict):
            raise RuntimeError('runtime_refusal:schema_invalid')
        encoded = json.dumps(request, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
        if len(encoded) > bundle_contract.runtime_request_limits['max_request_bytes']:
            raise RuntimeError('runtime_refusal:request_too_large')

    def evaluate_only(self, request: dict[str, Any]) -> dict[str, Any]:
        self.validate_request(request)
        result = evaluate_profile(self.profile, request)
        return {
            'bundle_digest': self.bundle_digest,
            'request_digest': digest_data(request),
            'verdict': result.verdict,
            'decisive_rule_ids': list(result.decisive_rule_ids),
            'matched': list(result.matched),
            'failed': list(result.failed),
            'fail_closed': result.fail_closed,
        }

class SealedBoundaryRunner:
    def __init__(self, bundle_dir: str | Path):
        self.runtime = _InternalVerifiedRuntime(bundle_dir)

    def execute(self, request: dict[str, Any], action_descriptor: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(action_descriptor, dict) or sorted(action_descriptor.keys()) != ['action_id', 'kind', 'payload']:
            raise RuntimeError('runtime_refusal:action_descriptor_invalid')
        verdict = self.runtime.evaluate_only(request)
        request_digest = digest_data(request)
        action_digest = digest_data(action_descriptor)
        if verdict['verdict'] != 'ALLOW':
            audit = make_refusal(
                code=REFUSAL_CODES['verdict_not_allow'],
                layer='action',
                bundle_digest=self.runtime.bundle_digest,
                request_digest=request_digest,
                action_digest=action_digest,
                permit_binding=None,
                details={'decisive_rule_ids': verdict['decisive_rule_ids']},
            )
            audit = attach_witness_certificate(audit)
            with self.runtime.audit_log_path.open('a', encoding='utf-8') as fh:
                fh.write(json.dumps(audit, sort_keys=True) + '\n')
            return audit
        permit = {
            'primitive_identity': PRIMITIVE_IDENTITY,
            'bundle_digest': self.runtime.bundle_digest,
            'request_digest': request_digest,
            'action_digest': action_digest,
            'permit': True,
            'verdict': 'ALLOW',
            'permit_type': 'ACTION_DESCRIPTOR_RELEASE',
            'released_action': action_descriptor,
            'action_authority': {
                'kind': 'release_bound_action_descriptor',
                'action_id': action_descriptor['action_id'],
                'action_kind': action_descriptor['kind'],
            },
            'permit_binding': {
                'primitive_identity': PRIMITIVE_IDENTITY,
                'bundle_digest': self.runtime.bundle_digest,
                'request_digest': request_digest,
                'action_digest': action_digest,
            },
            'replay_binding': {
                'primitive_identity': PRIMITIVE_IDENTITY,
                'bundle_digest': self.runtime.bundle_digest,
                'request_digest': request_digest,
            },
            'decisive_rule_ids': verdict['decisive_rule_ids'],
        }
        permit = attach_witness_certificate(permit)
        with self.runtime.audit_log_path.open('a', encoding='utf-8') as fh:
            fh.write(json.dumps(permit, sort_keys=True) + '\n')
        return permit

def refuse_non_bypass(bundle_dir: str | Path, request: dict[str, Any], attempted_entrypoint: str) -> dict[str, Any]:
    runtime = _InternalVerifiedRuntime(bundle_dir)
    request_digest = digest_data(request)
    return attach_witness_certificate(make_refusal(
        code=REFUSAL_CODES['non_bypass_violation'],
        layer='runtime',
        bundle_digest=runtime.bundle_digest,
        request_digest=request_digest,
        attempted_entrypoint=attempted_entrypoint,
    ))
