from __future__ import annotations
from typing import Any, Final

from .witness_certificate import WITNESS_CERTIFICATE_SCHEMA

PRIMITIVE_IDENTITY: Final[str] = 'BCF Primitive One'

WITNESS_CERTIFICATE_REF: Final[dict[str, object]] = WITNESS_CERTIFICATE_SCHEMA


REFUSAL_TAXONOMY: Final[dict[str, object]] = {
    'title': 'BCF Primitive One Refusal Taxonomy',
    'version': 'BCF_PRIMITIVE_ONE_CONTRACT_V1',
    'classes': {
        'primitive_identity': ['REFUSE_PRIMITIVE_IDENTITY_INVALID'],
        'canonicalization': ['REFUSE_CANONICALIZATION_FAILED'],
        'verification': [
            'REFUSE_REQUIRED_FILES_MISSING',
            'REFUSE_UNDECLARED_FILE',
            'REFUSE_CONTRACT_MISMATCH',
            'REFUSE_MANIFEST_MISMATCH',
            'REFUSE_COMPILER_PRODUCT_MISMATCH',
            'REFUSE_CERTIFICATE_INVALID',
            'REFUSE_GOVERNANCE_INVALID',
            'REFUSE_VERDICT_SCHEMA_INVALID',
            'REFUSE_VERIFICATION_SCHEMA_INVALID',
            'REFUSE_REFUSAL_SCHEMA_INVALID',
            'REFUSE_PERMIT_SCHEMA_INVALID',
            'REFUSE_COMPILED_BACKEND_SCHEMA_INVALID',
            'REFUSE_CLAIM_TCB_INVALID',
            'REFUSE_CLAIM_MATRIX_INVALID',
            'REFUSE_WITNESS_REPLAY_FAILED',
            'REFUSE_BUNDLE_VERIFICATION_FAILED',
        ],
        'request_shape': ['REFUSE_SCHEMA_INVALID'],
        'request_bounds': ['REFUSE_REQUEST_OVERSIZE'],
        'action_binding': ['REFUSE_ACTION_DESCRIPTOR_INVALID'],
        'contract_satisfaction': ['REFUSE_VERDICT_NOT_ALLOW'],
        'non_bypass': ['REFUSE_NON_BYPASS_VIOLATION'],
        'equivalence': ['REFUSE_EQUIVALENCE_PARITY_FAILED'],
    },
}

_ALL_CODES = [code for codes in REFUSAL_TAXONOMY['classes'].values() for code in codes]
CODE_TO_CLASS: Final[dict[str, str]] = {code: cls for cls, codes in REFUSAL_TAXONOMY['classes'].items() for code in codes}

REFUSAL_SCHEMA: Final[dict[str, object]] = {
    '$schema': 'https://json-schema.org/draft/2020-12/schema',
    'title': 'BCF Refusal Event',
    'type': 'object',
    'required': ['primitive_identity', 'permit', 'verdict', 'refusal_code', 'refusal_class', 'layer', 'replay_binding'],
    'properties': {
        'primitive_identity': {'type': 'string', 'const': PRIMITIVE_IDENTITY},
        'bundle_digest': {'type': ['string', 'null']},
        'request_digest': {'type': ['string', 'null']},
        'action_digest': {'type': ['string', 'null']},
        'permit': {'type': 'boolean', 'const': False},
        'verdict': {'enum': ['REFUSAL']},
        'refusal_code': {'enum': _ALL_CODES},
        'refusal_class': {'enum': list(REFUSAL_TAXONOMY['classes'].keys())},
        'layer': {'enum': ['bundle', 'runtime', 'action', 'equivalence']},
        'attempted_entrypoint': {'type': 'string'},
        'verification_result': {'enum': ['NOT_VERIFIED']},
        'permit_binding': {'type': ['object', 'null']},
        'replay_binding': {
            'type': 'object',
            'required': ['primitive_identity'],
            'properties': {
                'primitive_identity': {'type': 'string', 'const': PRIMITIVE_IDENTITY},
                'bundle_digest': {'type': ['string', 'null']},
                'request_digest': {'type': ['string', 'null']},
            },
            'additionalProperties': True,
        },
        'refusal_reasons': {'type': 'array', 'items': {'enum': _ALL_CODES}},
        'details': {'type': 'object'},
        'checks': {'type': 'object'},
        'witness_certificate': WITNESS_CERTIFICATE_REF,
        'overall_ok': {'type': 'boolean', 'const': False},
    },
    'additionalProperties': True,
}

PERMIT_SCHEMA: Final[dict[str, object]] = {
    '$schema': 'https://json-schema.org/draft/2020-12/schema',
    'title': 'BCF Permit Event',
    'type': 'object',
    'required': ['primitive_identity', 'permit', 'verdict', 'permit_type', 'permit_binding', 'action_authority', 'replay_binding'],
    'properties': {
        'primitive_identity': {'type': 'string', 'const': PRIMITIVE_IDENTITY},
        'bundle_digest': {'type': 'string'},
        'request_digest': {'type': 'string'},
        'action_digest': {'type': 'string'},
        'permit': {'type': 'boolean', 'const': True},
        'verdict': {'enum': ['ALLOW']},
        'permit_type': {'enum': ['ACTION_DESCRIPTOR_RELEASE']},
        'released_action': {'type': 'object'},
        'action_authority': {
            'type': 'object',
            'required': ['kind', 'action_id', 'action_kind'],
            'properties': {
                'kind': {'enum': ['release_bound_action_descriptor']},
                'action_id': {'type': 'string'},
                'action_kind': {'type': 'string'},
            },
            'additionalProperties': True,
        },
        'permit_binding': {
            'type': 'object',
            'required': ['primitive_identity', 'bundle_digest', 'request_digest', 'action_digest'],
            'properties': {
                'primitive_identity': {'type': 'string', 'const': PRIMITIVE_IDENTITY},
                'bundle_digest': {'type': 'string'},
                'request_digest': {'type': 'string'},
                'action_digest': {'type': 'string'},
            },
            'additionalProperties': True,
        },
        'replay_binding': {
            'type': 'object',
            'required': ['primitive_identity', 'bundle_digest', 'request_digest'],
            'properties': {
                'primitive_identity': {'type': 'string', 'const': PRIMITIVE_IDENTITY},
                'bundle_digest': {'type': 'string'},
                'request_digest': {'type': 'string'},
            },
            'additionalProperties': True,
        },
        'decisive_rule_ids': {'type': 'array', 'items': {'type': 'string'}},
        'witness_certificate': WITNESS_CERTIFICATE_REF,
    },
    'additionalProperties': True,
}

VERIFICATION_RESULT_SCHEMA: Final[dict[str, object]] = {
    '$schema': 'https://json-schema.org/draft/2020-12/schema',
    'title': 'BCF Verification Result',
    'oneOf': [
        {
            'type': 'object',
            'required': ['primitive_identity', 'verification_result', 'overall_ok', 'bundle_digest', 'checks', 'details', 'replay_binding'],
            'properties': {
                'primitive_identity': {'type': 'string', 'const': PRIMITIVE_IDENTITY},
                'verification_result': {'enum': ['VERIFIED']},
                'overall_ok': {'type': 'boolean', 'const': True},
                'bundle_digest': {'type': 'string'},
                'checks': {'type': 'object'},
        'witness_certificate': WITNESS_CERTIFICATE_REF,
                'details': {'type': 'object'},
                'witness_certificate': WITNESS_CERTIFICATE_REF,
                'replay_binding': {
                    'type': 'object',
                    'required': ['primitive_identity', 'bundle_digest', 'request_digest'],
                    'properties': {
                        'primitive_identity': {'type': 'string', 'const': PRIMITIVE_IDENTITY},
                        'bundle_digest': {'type': 'string'},
                        'request_digest': {'type': 'null'},
                    },
                    'additionalProperties': True,
                },
            },
            'additionalProperties': True,
        },
        REFUSAL_SCHEMA,
    ],
}


def refusal_class_for_code(code: str) -> str:
    if code not in CODE_TO_CLASS:
        raise KeyError(code)
    return CODE_TO_CLASS[code]


def make_refusal(
    *, code: str, layer: str, bundle_digest: str | None, request_digest: str | None = None, action_digest: str | None = None,
    attempted_entrypoint: str | None = None, verification_result: str | None = None, refusal_reasons: list[str] | None = None,
    details: dict[str, Any] | None = None, permit_binding: dict[str, Any] | None = None,
) -> dict[str, Any]:
    refusal = {
        'primitive_identity': PRIMITIVE_IDENTITY,
        'bundle_digest': bundle_digest,
        'request_digest': request_digest,
        'action_digest': action_digest,
        'permit': False,
        'verdict': 'REFUSAL',
        'refusal_code': code,
        'refusal_class': refusal_class_for_code(code),
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
