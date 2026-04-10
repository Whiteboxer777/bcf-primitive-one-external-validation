from __future__ import annotations

from typing import Any

from .common import PRIMITIVE_IDENTITY

CODE_TO_CLASS: dict[str, str] = {
    'REFUSE_PRIMITIVE_IDENTITY_INVALID': 'primitive_identity',
    'REFUSE_CANONICALIZATION_FAILED': 'canonicalization',
    'REFUSE_REQUIRED_FILES_MISSING': 'verification',
    'REFUSE_UNDECLARED_FILE': 'verification',
    'REFUSE_CONTRACT_MISMATCH': 'verification',
    'REFUSE_MANIFEST_MISMATCH': 'verification',
    'REFUSE_COMPILER_PRODUCT_MISMATCH': 'verification',
    'REFUSE_CERTIFICATE_INVALID': 'verification',
    'REFUSE_GOVERNANCE_INVALID': 'verification',
    'REFUSE_VERDICT_SCHEMA_INVALID': 'verification',
    'REFUSE_VERIFICATION_SCHEMA_INVALID': 'verification',
    'REFUSE_REFUSAL_SCHEMA_INVALID': 'verification',
    'REFUSE_PERMIT_SCHEMA_INVALID': 'verification',
    'REFUSE_CLAIM_TCB_INVALID': 'verification',
    'REFUSE_CLAIM_MATRIX_INVALID': 'verification',
    'REFUSE_WITNESS_REPLAY_FAILED': 'verification',
    'REFUSE_BUNDLE_VERIFICATION_FAILED': 'verification',
    'REFUSE_SCHEMA_INVALID': 'request_shape',
    'REFUSE_REQUEST_OVERSIZE': 'request_bounds',
    'REFUSE_ACTION_DESCRIPTOR_INVALID': 'action_binding',
    'REFUSE_VERDICT_NOT_ALLOW': 'contract_satisfaction',
    'REFUSE_NON_BYPASS_VIOLATION': 'non_bypass',
    'REFUSE_EQUIVALENCE_PARITY_FAILED': 'equivalence',
}


def make_refusal(
    *,
    code: str,
    layer: str,
    bundle_digest: str | None,
    request_digest: str | None = None,
    action_digest: str | None = None,
    attempted_entrypoint: str | None = None,
    verification_result: str | None = None,
    refusal_reasons: list[str] | None = None,
    details: dict[str, Any] | None = None,
    permit_binding: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if code not in CODE_TO_CLASS:
        raise KeyError(code)
    refusal: dict[str, Any] = {
        'primitive_identity': PRIMITIVE_IDENTITY,
        'bundle_digest': bundle_digest,
        'request_digest': request_digest,
        'action_digest': action_digest,
        'permit': False,
        'verdict': 'REFUSAL',
        'refusal_code': code,
        'refusal_class': CODE_TO_CLASS[code],
        'layer': layer,
        'permit_binding': permit_binding,
        'replay_binding': {
            'primitive_identity': PRIMITIVE_IDENTITY,
            'bundle_digest': bundle_digest,
            'request_digest': request_digest,
        },
    }
    if attempted_entrypoint is not None:
        refusal['attempted_entrypoint'] = attempted_entrypoint
    if verification_result is not None:
        refusal['verification_result'] = verification_result
    if refusal_reasons is not None:
        refusal['refusal_reasons'] = list(refusal_reasons)
    if details:
        refusal['details'] = details
    return refusal


def make_permit(*, bundle_digest: str, request_digest: str, action: dict[str, Any], decisive_rule_ids: list[str]) -> dict[str, Any]:
    action_digest = __import__('hashlib').sha256(__import__('json').dumps(action, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')).hexdigest()
    return {
        'primitive_identity': PRIMITIVE_IDENTITY,
        'bundle_digest': bundle_digest,
        'request_digest': request_digest,
        'action_digest': action_digest,
        'permit': True,
        'verdict': 'ALLOW',
        'permit_type': 'ACTION_DESCRIPTOR_RELEASE',
        'released_action': action,
        'action_authority': {
            'kind': 'release_bound_action_descriptor',
            'action_id': action['action_id'],
            'action_kind': action['kind'],
        },
        'permit_binding': {
            'primitive_identity': PRIMITIVE_IDENTITY,
            'bundle_digest': bundle_digest,
            'request_digest': request_digest,
            'action_digest': action_digest,
        },
        'replay_binding': {
            'primitive_identity': PRIMITIVE_IDENTITY,
            'bundle_digest': bundle_digest,
            'request_digest': request_digest,
        },
        'decisive_rule_ids': list(decisive_rule_ids),
    }
