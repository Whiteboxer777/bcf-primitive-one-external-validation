from __future__ import annotations

from typing import Any, Final

from .common import digest_data

PRIMITIVE_IDENTITY: Final[str] = 'BCF Primitive One'

CERTIFICATE_VERSION: Final[str] = 'WITNESS_CERT_V2'
CERTIFICATE_SCOPE: Final[str] = 'kernel_evidence_carrying_v2'
SOURCE_KINDS: Final[tuple[str, ...]] = (
    'verification_result',
    'permit',
    'refusal',
    'replay_allow',
    'replay_refusal',
    'non_bypass_refusal',
)

_SHARED_WITNESS_CLAIMS: Final[dict[str, object]] = {
    'type': 'object',
    'required': ['witness_kind', 'witness_scope', 'binding_kind', 'claim_set_digest'],
    'properties': {
        'witness_kind': {'enum': ['verification', 'permit', 'refusal']},
        'witness_scope': {
            'enum': [
                'bundle_verification',
                'action_release',
                'action_refusal',
                'bundle_refusal',
                'runtime_refusal',
                'replay_allow',
                'replay_refusal',
                'non_bypass_refusal',
            ]
        },
        'binding_kind': {'enum': ['bundle_only', 'action_release', 'replay', 'bundle_failure', 'runtime_failure', 'non_bypass']},
        'claim_set_digest': {'type': 'string'},
        'verification_result': {'enum': ['VERIFIED', 'NOT_VERIFIED']},
        'refusal_code': {'type': 'string'},
        'refusal_class': {'type': 'string'},
        'refusal_reasons_digest': {'type': 'string'},
        'action_authority_kind': {'type': ['string', 'null']},
        'decisive_rule_ids': {'type': 'array', 'items': {'type': 'string'}},
        'decisive_rule_ids_digest': {'type': 'string'},
        'permit_binding_digest': {'type': 'string'},
        'checks_digest': {'type': 'string'},
        'details_digest': {'type': 'string'},
        'check_truth_count': {'type': 'integer', 'minimum': 0},
    },
    'additionalProperties': False,
    'allOf': [
        {
            'if': {'properties': {'witness_kind': {'const': 'verification'}}},
            'then': {
                'required': ['verification_result', 'checks_digest', 'details_digest', 'check_truth_count'],
            },
        },
        {
            'if': {'properties': {'witness_kind': {'const': 'permit'}}},
            'then': {
                'required': ['action_authority_kind', 'decisive_rule_ids', 'decisive_rule_ids_digest', 'permit_binding_digest'],
            },
        },
        {
            'if': {'properties': {'witness_kind': {'const': 'refusal'}}},
            'then': {
                'required': ['refusal_code', 'refusal_class', 'refusal_reasons_digest', 'details_digest'],
            },
        },
    ],
}

WITNESS_CERTIFICATE_SCHEMA: Final[dict[str, object]] = {
    '$schema': 'https://json-schema.org/draft/2020-12/schema',
    'title': 'BCF Primitive One Witness Certificate',
    'type': 'object',
    'required': [
        'primitive_identity',
        'certificate_version',
        'certificate_scope',
        'certificate_type',
        'source_verdict',
        'source_kind',
        'bundle_digest',
        'source_digest',
        'binding_digest',
        'witness_claims',
        'certificate_digest',
    ],
    'properties': {
        'primitive_identity': {'type': 'string', 'const': PRIMITIVE_IDENTITY},
        'certificate_version': {'type': 'string', 'const': CERTIFICATE_VERSION},
        'certificate_scope': {'type': 'string', 'const': CERTIFICATE_SCOPE},
        'certificate_type': {'enum': ['verification_witness', 'permit_witness', 'refusal_witness']},
        'source_verdict': {'enum': ['VERIFIED', 'ALLOW', 'REFUSAL']},
        'source_kind': {'enum': list(SOURCE_KINDS)},
        'bundle_digest': {'type': ['string', 'null']},
        'request_digest': {'type': ['string', 'null']},
        'action_digest': {'type': ['string', 'null']},
        'source_digest': {'type': 'string'},
        'binding_digest': {'type': ['string', 'null']},
        'witness_claims': _SHARED_WITNESS_CLAIMS,
        'certificate_digest': {'type': 'string'},
    },
    'additionalProperties': False,
}


def strip_witness_certificate(payload: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in payload.items() if k != 'witness_certificate'}


def _binding_payload(source: dict[str, Any]) -> dict[str, Any] | None:
    if isinstance(source.get('permit_binding'), dict):
        return source['permit_binding']
    if isinstance(source.get('replay_binding'), dict):
        return source['replay_binding']
    if source.get('bundle_digest') is not None:
        return {
            'primitive_identity': PRIMITIVE_IDENTITY,
            'bundle_digest': source.get('bundle_digest'),
            'request_digest': source.get('request_digest'),
            'action_digest': source.get('action_digest'),
        }
    return None


def _finalize_claims(claims: dict[str, Any]) -> dict[str, Any]:
    body = dict(claims)
    body['claim_set_digest'] = digest_data(body)
    return body


def build_witness_certificate(*, certificate_type: str, source_verdict: str, source_kind: str, payload: dict[str, Any], witness_claims: dict[str, Any]) -> dict[str, Any]:
    source = strip_witness_certificate(payload)
    binding_payload = _binding_payload(source)
    body = {
        'primitive_identity': PRIMITIVE_IDENTITY,
        'certificate_version': CERTIFICATE_VERSION,
        'certificate_scope': CERTIFICATE_SCOPE,
        'certificate_type': certificate_type,
        'source_verdict': source_verdict,
        'source_kind': source_kind,
        'bundle_digest': source.get('bundle_digest'),
        'request_digest': source.get('request_digest'),
        'action_digest': source.get('action_digest'),
        'source_digest': digest_data(source),
        'binding_digest': digest_data(binding_payload) if binding_payload is not None else None,
        'witness_claims': _finalize_claims(witness_claims),
    }
    body['certificate_digest'] = digest_data(body)
    return body


def _verification_witness_claims(source: dict[str, Any]) -> dict[str, Any]:
    checks = source.get('checks', {}) if isinstance(source.get('checks'), dict) else {}
    details = source.get('details', {}) if isinstance(source.get('details'), dict) else {}
    return {
        'witness_kind': 'verification',
        'witness_scope': 'bundle_verification',
        'binding_kind': 'bundle_only',
        'verification_result': source.get('verification_result', 'VERIFIED'),
        'checks_digest': digest_data(checks),
        'details_digest': digest_data(details),
        'check_truth_count': sum(1 for v in checks.values() if v is True),
    }


def _permit_witness_claims(source: dict[str, Any], *, replay: bool = False) -> dict[str, Any]:
    decisive_rule_ids = list(source.get('decisive_rule_ids', []))
    binding = source.get('permit_binding') if isinstance(source.get('permit_binding'), dict) else source.get('replay_binding', {})
    return {
        'witness_kind': 'permit',
        'witness_scope': 'replay_allow' if replay else 'action_release',
        'binding_kind': 'replay' if replay else 'action_release',
        'action_authority_kind': source.get('action_authority', {}).get('kind') if isinstance(source.get('action_authority'), dict) else None,
        'decisive_rule_ids': decisive_rule_ids,
        'decisive_rule_ids_digest': digest_data(decisive_rule_ids),
        'permit_binding_digest': digest_data(binding),
    }


def _refusal_witness_claims(source: dict[str, Any], *, scope: str, binding_kind: str) -> dict[str, Any]:
    refusal_reasons = list(source.get('refusal_reasons', []))
    details = source.get('details', {}) if isinstance(source.get('details'), dict) else {}
    return {
        'witness_kind': 'refusal',
        'witness_scope': scope,
        'binding_kind': binding_kind,
        'refusal_code': source.get('refusal_code'),
        'refusal_class': source.get('refusal_class'),
        'refusal_reasons_digest': digest_data(refusal_reasons),
        'details_digest': digest_data(details),
    }


def attach_witness_certificate(payload: dict[str, Any]) -> dict[str, Any]:
    source = strip_witness_certificate(payload)
    if source.get('verification_result') == 'VERIFIED':
        cert = build_witness_certificate(
            certificate_type='verification_witness',
            source_verdict='VERIFIED',
            source_kind='verification_result',
            payload=source,
            witness_claims=_verification_witness_claims(source),
        )
    elif source.get('verdict') == 'ALLOW' and isinstance(source.get('action_authority'), dict):
        cert = build_witness_certificate(
            certificate_type='permit_witness',
            source_verdict='ALLOW',
            source_kind='permit',
            payload=source,
            witness_claims=_permit_witness_claims(source, replay=False),
        )
    elif source.get('verdict') == 'ALLOW':
        cert = build_witness_certificate(
            certificate_type='permit_witness',
            source_verdict='ALLOW',
            source_kind='replay_allow',
            payload=source,
            witness_claims=_permit_witness_claims(source, replay=True),
        )
    else:
        attempted = source.get('attempted_entrypoint')
        if attempted is not None:
            source_kind = 'non_bypass_refusal'
            scope = 'non_bypass_refusal'
            binding_kind = 'non_bypass'
        elif source.get('layer') == 'bundle' or source.get('verification_result') == 'NOT_VERIFIED':
            source_kind = 'refusal' if source.get('source_kind') == 'refusal' else 'refusal'
            scope = 'bundle_refusal'
            binding_kind = 'bundle_failure'
        elif source.get('layer') == 'runtime':
            source_kind = 'replay_refusal'
            scope = 'replay_refusal'
            binding_kind = 'replay'
        else:
            source_kind = 'refusal'
            scope = 'action_refusal'
            binding_kind = 'action_release'
        cert = build_witness_certificate(
            certificate_type='refusal_witness',
            source_verdict='REFUSAL',
            source_kind=source_kind,
            payload=source,
            witness_claims=_refusal_witness_claims(source, scope=scope, binding_kind=binding_kind),
        )
    enriched = dict(source)
    enriched['witness_certificate'] = cert
    return enriched
