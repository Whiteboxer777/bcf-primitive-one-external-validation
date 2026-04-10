from __future__ import annotations

import base64
import hashlib
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

from .common import canonical_bytes

_DEV_SEEDS = {
    'root_prod': 'bcf-primitive-one-root-prod-seed',
    'root_stage': 'bcf-primitive-one-root-stage-seed',
}


def _seed_bytes(seed: str) -> bytes:
    return hashlib.sha256(seed.encode('utf-8')).digest()


def _b64(b: bytes) -> str:
    return base64.b64encode(b).decode('ascii')


def _ub64(s: str) -> bytes:
    return base64.b64decode(s.encode('ascii'))


def development_keyring() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for signer_id, seed in _DEV_SEEDS.items():
        priv = Ed25519PrivateKey.from_private_bytes(_seed_bytes(seed))
        pub = priv.public_key()
        out[signer_id] = {
            'algorithm': 'Ed25519',
            'private_key_b64': _b64(priv.private_bytes_raw()),
            'public_key_b64': _b64(pub.public_bytes_raw()),
        }
    return out


def default_trust_roots() -> dict[str, Any]:
    keyring = development_keyring()
    return {
        'version': 1,
        'roots': {
            'root_prod': {
                'algorithm': 'Ed25519',
                'public_key_b64': keyring['root_prod']['public_key_b64'],
                'roles': ['promotion_root', 'bundle_signer'],
                'scopes': ['production', 'staging'],
            },
            'root_stage': {
                'algorithm': 'Ed25519',
                'public_key_b64': keyring['root_stage']['public_key_b64'],
                'roles': ['bundle_signer'],
                'scopes': ['staging'],
            },
        },
    }


def default_authority_policy() -> dict[str, Any]:
    return {
        'version': 1,
        'required_role': 'bundle_signer',
        'allowed_scopes': {
            'CERTIFIED_FOR_PRODUCTION': ['production'],
            'ACCEPTED_FOR_STAGING': ['staging', 'production'],
            'QUARANTINED': ['staging', 'production'],
        },
        'minimum_signatures': {
            'CERTIFIED_FOR_PRODUCTION': 1,
            'ACCEPTED_FOR_STAGING': 1,
            'QUARANTINED': 1,
        },
    }


def default_revocation_list() -> dict[str, Any]:
    return {'version': 1, 'revoked_signers': [], 'revoked_signatures': []}


def _signature_payload(bundle_digest: str, promotion_cert_digest: str, signer_id: str, scope: str) -> bytes:
    return canonical_bytes({
        'bundle_digest': bundle_digest,
        'promotion_cert_digest': promotion_cert_digest,
        'signer_id': signer_id,
        'scope': scope,
    })


def sign_bundle(bundle_digest: str, promotion_cert: dict[str, Any], signer_id: str, scope: str) -> dict[str, Any]:
    keyring = development_keyring()
    priv = Ed25519PrivateKey.from_private_bytes(_ub64(keyring[signer_id]['private_key_b64']))
    payload = _signature_payload(bundle_digest, promotion_cert['cert_digest'], signer_id, scope)
    signature = priv.sign(payload)
    return {
        'signer_id': signer_id,
        'algorithm': 'Ed25519',
        'scope': scope,
        'bundle_digest': bundle_digest,
        'promotion_cert_digest': promotion_cert['cert_digest'],
        'payload_digest': hashlib.sha256(payload).hexdigest(),
        'signature_b64': _b64(signature),
    }


def verify_signature(signature_record: dict[str, Any], trust_roots: dict[str, Any], revocation_list: dict[str, Any]) -> dict[str, Any]:
    signer_id = signature_record.get('signer_id')
    roots = trust_roots.get('roots', {})
    if signer_id not in roots:
        return {'ok': False, 'reason': 'unknown_signer', 'signer_id': signer_id}
    if signer_id in set(revocation_list.get('revoked_signers', [])):
        return {'ok': False, 'reason': 'signer_revoked', 'signer_id': signer_id}
    if signature_record.get('payload_digest') in set(revocation_list.get('revoked_signatures', [])):
        return {'ok': False, 'reason': 'signature_revoked', 'signer_id': signer_id}
    payload = _signature_payload(signature_record['bundle_digest'], signature_record['promotion_cert_digest'], signer_id, signature_record['scope'])
    try:
        pub = Ed25519PublicKey.from_public_bytes(_ub64(roots[signer_id]['public_key_b64']))
        pub.verify(_ub64(signature_record['signature_b64']), payload)
        return {'ok': True, 'reason': 'verified', 'signer_id': signer_id, 'scope': signature_record.get('scope')}
    except InvalidSignature:
        return {'ok': False, 'reason': 'invalid_signature', 'signer_id': signer_id}


def evaluate_authority(signatures: list[dict[str, Any]], trust_roots: dict[str, Any], authority_policy: dict[str, Any], promotion_verdict: str) -> dict[str, Any]:
    req_role = authority_policy.get('required_role', 'bundle_signer')
    allowed_scopes = set(authority_policy.get('allowed_scopes', {}).get(promotion_verdict, []))
    min_sigs = int(authority_policy.get('minimum_signatures', {}).get(promotion_verdict, 1))
    approved: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for sig in signatures:
        signer = trust_roots.get('roots', {}).get(sig.get('signer_id'), {})
        roles = set(signer.get('roles', []))
        signer_scopes = set(signer.get('scopes', []))
        scope = sig.get('scope')
        reasons: list[str] = []
        if req_role not in roles:
            reasons.append('missing_required_role')
        if scope not in allowed_scopes:
            reasons.append('scope_not_allowed_for_verdict')
        if scope not in signer_scopes:
            reasons.append('scope_not_allowed_for_signer')
        rec = {'signer_id': sig.get('signer_id'), 'scope': scope, 'ok': not reasons, 'reasons': reasons}
        if reasons:
            rejected.append(rec)
        else:
            approved.append(rec)
    return {
        'ok': len(approved) >= min_sigs,
        'minimum_required': min_sigs,
        'approved': approved,
        'rejected': rejected,
    }


def tcb_report() -> dict[str, Any]:
    trusted_components = [
        "strict_json parser",
        "profile parser",
        "canonicalization and digest engine",
        "normalizer",
        "minimizer",
        "satisfiability and relation enumerator",
        "witness replay checker",
        "manifest verifier",
        "governance signature verifier",
        "authority policy evaluator",
        "sealed runtime request-size gate",
        "sealed action descriptor validator",
    ]
    return {
        "version": "1.0.0",
        "trusted_components": trusted_components,
        "trusted_component_count": len(trusted_components),
        "excluded_from_tcb": [
            "legacy source tree outside primitive identity",
            "historical release notes",
            "parallel bundle families",
            "pycache and build leftovers",
            "development-only scaffolding outside official route",
        ],
        "reduction_status": "primitive_one_reference_tcb",
        "language": "Python",
        "hardening_level": "primitive_one_reference",
        "official_runner_only": True,
    }
