from __future__ import annotations
from pathlib import Path
from .common import digest_data, load_json
from .contract import bundle_contract
from .kernel_support import evaluate_profile, parse_profile
from .refusal import PRIMITIVE_IDENTITY, make_refusal
from .verifier import verify_bundle
from .witness_certificate import attach_witness_certificate


def replay_verdict(bundle_dir: str | Path, request: dict[str, object]) -> dict[str, object]:
    bundle = Path(bundle_dir)
    verification_report = verify_bundle(bundle)
    if not verification_report.get('overall_ok', False):
        return attach_witness_certificate(make_refusal(
            code=verification_report.get('refusal_code', 'REFUSE_BUNDLE_VERIFICATION_FAILED'),
            layer='bundle',
            bundle_digest=verification_report.get('bundle_digest'),
            request_digest=digest_data(request),
            verification_result='NOT_VERIFIED',
            refusal_reasons=verification_report.get('refusal_reasons', ['REFUSE_BUNDLE_VERIFICATION_FAILED']),
            details={'source': 'replay_verdict'},
        ) | {'overall_ok': False})
    profile = parse_profile(load_json(bundle / 'PROFILE_SOURCE.json'))
    manifest = load_json(bundle / bundle_contract.manifest_name)
    bundle_digest = digest_data(manifest)
    result = evaluate_profile(profile, request)
    if result.verdict != 'ALLOW':
        return attach_witness_certificate(make_refusal(
            code='REFUSE_VERDICT_NOT_ALLOW',
            layer='runtime',
            bundle_digest=bundle_digest,
            request_digest=digest_data(request),
            refusal_reasons=['REFUSE_VERDICT_NOT_ALLOW'],
            details={
                'source': 'replay_verdict',
                'decisive_rule_ids': list(result.decisive_rule_ids),
                'matched': list(result.matched),
                'failed': list(result.failed),
                'fail_closed': result.fail_closed,
            },
        ) | {'overall_ok': False})
    return attach_witness_certificate({
        'primitive_identity': PRIMITIVE_IDENTITY,
        'overall_ok': True,
        'bundle_digest': bundle_digest,
        'request_digest': digest_data(request),
        'verdict': result.verdict,
        'replay_binding': {'primitive_identity': PRIMITIVE_IDENTITY, 'bundle_digest': bundle_digest, 'request_digest': digest_data(request)},
        'decisive_rule_ids': list(result.decisive_rule_ids),
        'matched': list(result.matched),
        'failed': list(result.failed),
        'fail_closed': result.fail_closed,
    })
