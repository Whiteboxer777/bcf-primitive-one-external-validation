from __future__ import annotations
from pathlib import Path
from typing import Any
from .common import digest_data, load_json, sha256_file
from .contract import VERDICT_SCHEMA, bundle_contract
from .governance import evaluate_authority, verify_signature
from .kernel_support import compare_profiles, evaluate_profile, extract_decisive_core, is_satisfiable, minimize_profile, normalize, parse_profile, Profile
from .refusal import REFUSAL_SCHEMA, PERMIT_SCHEMA, VERIFICATION_RESULT_SCHEMA, PRIMITIVE_IDENTITY, make_refusal
from .witness_certificate import WITNESS_CERTIFICATE_SCHEMA, attach_witness_certificate
from .admission_normal_form import compile_admission_normal_form
from .compiled_backend import compile_compiled_backend

def _verify_required_files(bundle: Path) -> dict[str, Any]:
    missing = [name for name in bundle_contract.required_files if not (bundle / name).exists()]
    return {'ok': not missing, 'missing': missing}

def _verify_no_forbidden_top_level(bundle: Path) -> dict[str, Any]:
    present = sorted(p.name for p in bundle.iterdir() if p.is_file())
    forbidden = [name for name in present if name not in bundle_contract.allowed_top_level_files]
    return {'ok': not forbidden, 'forbidden': forbidden, 'present': present}

def _verify_contract(bundle: Path) -> dict[str, Any]:
    data = load_json(bundle / 'BUNDLE_CONTRACT.json'); expected = bundle_contract.to_dict(); ok = data == expected; digest_ok = data.get('contract_digest') == expected.get('contract_digest')
    return {'ok': ok and digest_ok, 'claimed_version': data.get('contract_version'), 'expected_version': bundle_contract.version, 'digest_ok': digest_ok}

def _verify_manifest(bundle: Path) -> dict[str, Any]:
    manifest = load_json(bundle / bundle_contract.manifest_name); mismatches = []
    for rel in bundle_contract.manifest_scoped_files:
        expected = manifest.get(rel); actual = sha256_file(bundle / rel) if (bundle / rel).exists() else None
        if actual != expected: mismatches.append({'file': rel, 'expected': expected, 'actual': actual})
    extra = sorted(set(manifest) - set(bundle_contract.manifest_scoped_files))
    return {'ok': not mismatches and not extra, 'mismatches': mismatches, 'extra_manifest_entries': extra, 'bundle_digest': digest_data(manifest)}

def _verify_compiler_products(bundle: Path) -> dict[str, Any]:
    profile_data = load_json(bundle / 'PROFILE_SOURCE.json'); profile = parse_profile(profile_data); recomputed_norm = normalize(profile.root).node.to_dict(); recomputed_anf = compile_admission_normal_form(profile).to_dict(); recomputed_backend = compile_compiled_backend(profile).to_dict(); minimized = minimize_profile(profile); minimized_profile = Profile(profile.profile_id, profile.mode, minimized.root, profile.description, profile.analysis_domains); recomputed_sat = is_satisfiable(profile); recomputed_rel = compare_profiles(profile, minimized_profile).to_dict(); stored_sat = load_json(bundle / 'SAT_REPORT.json'); stored_rel = load_json(bundle / 'RELATION_REPORT.json')
    checks = {'normal_form': recomputed_norm == load_json(bundle / 'NORMAL_FORM.json'), 'admission_normal_form': recomputed_anf == load_json(bundle / 'ADMISSION_NORMAL_FORM.json'), 'compiled_backend': recomputed_backend == load_json(bundle / 'COMPILED_BACKEND.json'), 'minimized_form': minimized.root.to_dict() == load_json(bundle / 'MINIMIZED_FORM.json'), 'sat_report': {'satisfiable': recomputed_sat.satisfiable, 'universe_size': recomputed_sat.universe_size, 'witness': recomputed_sat.witness.to_dict() if recomputed_sat.witness else None} == stored_sat, 'relation_report': recomputed_rel == stored_rel, 'decisive_core_sample': extract_decisive_core(profile, load_json(bundle / 'WITNESS_SET.json')[0]['request']) == load_json(bundle / 'DECISIVE_CORE_SAMPLE.json')}
    return {'ok': all(bool(v) for v in checks.values()), 'checks': checks}

def _verify_certificates(bundle: Path) -> dict[str, Any]:
    cert_names = ['NORMALIZATION_CERT.json','MINIMIZATION_CERT.json','SAT_CERT.json','RELATION_CERT.json','CONFORMANCE_CERT.json','DECISIVE_CORE_CERT.json','PROMOTION_CERT.json']; details = {}
    for name in cert_names:
        cert = load_json(bundle / name); claims = {k: v for k, v in cert.items() if k != 'cert_digest'}; details[name] = {'ok': digest_data(claims) == cert.get('cert_digest')}
    return {'ok': all(v['ok'] for v in details.values()), 'details': details}

def _verify_governance(bundle: Path, manifest_digest: str) -> dict[str, Any]:
    trust = load_json(bundle / 'TRUST_ROOTS.json'); policy = load_json(bundle / 'AUTHORITY_POLICY.json'); revocations = load_json(bundle / 'REVOCATION_LIST.json'); promotion = load_json(bundle / 'PROMOTION_CERT.json'); signatures = load_json(bundle / 'PROMOTION_SIGNATURES.json').get('signatures', []); supersession = load_json(bundle / 'SUPERSESSION_CHAIN.json')
    sig_checks = [verify_signature(sig, trust, revocations) for sig in signatures]; authority = evaluate_authority(signatures, trust, policy, promotion['claims']['promotion_verdict']); promo_ok = promotion['claims']['bundle_digest'] == manifest_digest and promotion['claims']['manifest_digest'] == manifest_digest and promotion['claims']['contract_version'] == bundle_contract.version; supersession_ok = supersession.get('current_bundle_digest') == manifest_digest and supersession.get('promotion_cert_digest') == promotion.get('cert_digest')
    return {'ok': promo_ok and supersession_ok and all(x['ok'] for x in sig_checks) and authority['ok'], 'promotion_ok': promo_ok, 'supersession_ok': supersession_ok, 'signature_checks': sig_checks, 'authority': authority}

def _verify_verdict_schema(bundle: Path) -> dict[str, Any]:
    stored = load_json(bundle / bundle_contract.verdict_schema_name); return {'ok': stored == VERDICT_SCHEMA, 'schema_name': bundle_contract.verdict_schema_name}


def _verify_verification_schema(bundle: Path) -> dict[str, Any]:
    stored = load_json(bundle / bundle_contract.verification_schema_name); return {'ok': stored == VERIFICATION_RESULT_SCHEMA, 'schema_name': bundle_contract.verification_schema_name}

def _verify_refusal_schema(bundle: Path) -> dict[str, Any]:
    stored = load_json(bundle / bundle_contract.refusal_schema_name); return {'ok': stored == REFUSAL_SCHEMA, 'schema_name': bundle_contract.refusal_schema_name}

def _verify_permit_schema(bundle: Path) -> dict[str, Any]:
    stored = load_json(bundle / bundle_contract.permit_schema_name); return {'ok': stored == PERMIT_SCHEMA, 'schema_name': bundle_contract.permit_schema_name}

def _verify_compiled_backend_schema(bundle: Path) -> dict[str, Any]:
    stored = load_json(bundle / bundle_contract.compiled_backend_schema_name); return {'ok': stored.get('title') == 'BCF Primitive One Compiled Backend', 'schema_name': bundle_contract.compiled_backend_schema_name}

def _verify_witness_certificate_schema(bundle: Path) -> dict[str, Any]:
    stored = load_json(bundle / bundle_contract.witness_certificate_schema_name); return {'ok': stored == WITNESS_CERTIFICATE_SCHEMA, 'schema_name': bundle_contract.witness_certificate_schema_name}

def _verify_witness_certificates(bundle: Path) -> dict[str, Any]:
    names = ['VERIFICATION_WITNESS_CERT.json', 'PERMIT_WITNESS_CERT.json', 'REFUSAL_WITNESS_CERT.json', 'REPLAY_ALLOW_WITNESS_CERT.json', 'REPLAY_REFUSAL_WITNESS_CERT.json', 'NO_BYPASS_WITNESS_CERT.json']
    details = {}
    for name in names:
        cert = load_json(bundle / name)
        claims = {k: v for k, v in cert.items() if k != 'certificate_digest'}
        details[name] = {'ok': digest_data(claims) == cert.get('certificate_digest')}
    return {'ok': all(v['ok'] for v in details.values()), 'details': details}

def _verify_claim_and_tcb(bundle: Path) -> dict[str, Any]:
    claim = load_json(bundle / bundle_contract.claim_name); tcb = load_json(bundle / bundle_contract.tcb_report_name); claim_ok = claim.get('parallel_families') is False and claim.get('official_runner_only') is True and claim.get('direct_runtime_api_officially_supported') is False and claim.get('official_route') == 'source_profile -> canonical_bundle -> verify -> sealed_runner -> permit_or_refusal'; tcb_ok = tcb.get('official_runner_only') is True and tcb.get('reduction_status') == 'primitive_one_reference_tcb'
    return {'ok': claim_ok and tcb_ok, 'claim_ok': claim_ok, 'tcb_ok': tcb_ok}

def _verify_claim_matrix(bundle: Path) -> dict[str, Any]:
    matrix = load_json(bundle / bundle_contract.claim_matrix_name); claims = matrix.get('claims', []); ok = matrix.get('version') == bundle_contract.version and len(claims) >= 5 and all('claim_id' in x and 'tests' in x and 'artifacts' in x for x in claims)
    return {'ok': ok, 'claim_count': len(claims)}

def _verify_witnesses(bundle: Path) -> dict[str, Any]:
    profile = parse_profile(load_json(bundle / 'PROFILE_SOURCE.json')); witnesses = load_json(bundle / 'WITNESS_SET.json'); mismatches = []
    for item in witnesses:
        result = evaluate_profile(profile, item['request'])
        if result.verdict != item['verdict']: mismatches.append({'request': item['request'], 'expected': item['verdict'], 'actual': result.verdict})
    return {'ok': not mismatches, 'checked': len(witnesses), 'mismatches': mismatches}

REFUSAL_CODE_MAP = {
    'required_files': 'REFUSE_REQUIRED_FILES_MISSING',
    'top_level': 'REFUSE_UNDECLARED_FILE',
    'contract': 'REFUSE_CONTRACT_MISMATCH',
    'manifest': 'REFUSE_MANIFEST_MISMATCH',
    'compiler_products': 'REFUSE_COMPILER_PRODUCT_MISMATCH',
    'certificates': 'REFUSE_CERTIFICATE_INVALID',
    'governance': 'REFUSE_GOVERNANCE_INVALID',
    'verdict_schema': 'REFUSE_VERDICT_SCHEMA_INVALID',
    'verification_schema': 'REFUSE_VERIFICATION_SCHEMA_INVALID',
    'refusal_schema': 'REFUSE_REFUSAL_SCHEMA_INVALID',
    'permit_schema': 'REFUSE_PERMIT_SCHEMA_INVALID',
    'compiled_backend_schema': 'REFUSE_COMPILED_BACKEND_SCHEMA_INVALID',
    'witness_certificate_schema': 'REFUSE_CERTIFICATE_INVALID',
    'witness_certificates': 'REFUSE_CERTIFICATE_INVALID',
    'claim_and_tcb': 'REFUSE_CLAIM_TCB_INVALID',
    'claim_matrix': 'REFUSE_CLAIM_MATRIX_INVALID',
    'witness_replay': 'REFUSE_WITNESS_REPLAY_FAILED',
}

_PRECEDENCE = ['required_files', 'top_level', 'contract', 'manifest', 'compiler_products', 'certificates', 'governance', 'verdict_schema', 'verification_schema', 'refusal_schema', 'permit_schema', 'compiled_backend_schema', 'witness_certificate_schema', 'witness_certificates', 'claim_and_tcb', 'claim_matrix', 'witness_replay']

def _verification_result(*, bundle_digest: str | None, overall_ok: bool, checks: dict[str, bool], details: dict[str, Any], refusal_reasons: list[str]) -> dict[str, Any]:
    if overall_ok:
        return attach_witness_certificate({
            'primitive_identity': PRIMITIVE_IDENTITY,
            'verification_result': 'VERIFIED',
            'overall_ok': True,
            'bundle_digest': bundle_digest,
            'checks': checks,
            'details': details,
            'replay_binding': {'primitive_identity': PRIMITIVE_IDENTITY, 'bundle_digest': bundle_digest, 'request_digest': None},
        })
    primary_name = next(name for name in _PRECEDENCE if not checks.get(name, True))
    primary_code = REFUSAL_CODE_MAP[primary_name]
    refusal = make_refusal(
        code=primary_code,
        layer='bundle',
        bundle_digest=bundle_digest,
        verification_result='NOT_VERIFIED',
        refusal_reasons=refusal_reasons,
        details=details,
    )
    refusal.update({'overall_ok': False, 'checks': checks})
    return attach_witness_certificate(refusal)

def verify_bundle(bundle_dir: str | Path) -> dict[str, Any]:
    bundle = Path(bundle_dir)
    required = _verify_required_files(bundle)
    if not required['ok']:
        return _verification_result(
            bundle_digest=None,
            overall_ok=False,
            checks={'required_files': False},
            details={'required_files': required},
            refusal_reasons=['REFUSE_REQUIRED_FILES_MISSING'],
        )
    top_level = _verify_no_forbidden_top_level(bundle)
    contract = _verify_contract(bundle)
    manifest = _verify_manifest(bundle)
    compiler = _verify_compiler_products(bundle)
    certs = _verify_certificates(bundle)
    governance = _verify_governance(bundle, manifest['bundle_digest'])
    verdict_schema = _verify_verdict_schema(bundle)
    verification_schema = _verify_verification_schema(bundle)
    refusal_schema = _verify_refusal_schema(bundle)
    permit_schema = _verify_permit_schema(bundle)
    compiled_backend_schema = _verify_compiled_backend_schema(bundle)
    witness_certificate_schema = _verify_witness_certificate_schema(bundle)
    witness_certificates = _verify_witness_certificates(bundle)
    claim_tcb = _verify_claim_and_tcb(bundle)
    claim_matrix = _verify_claim_matrix(bundle)
    witnesses = _verify_witnesses(bundle)
    checks = {
        'required_files': required['ok'],
        'top_level': top_level['ok'],
        'contract': contract['ok'],
        'manifest': manifest['ok'],
        'compiler_products': compiler['ok'],
        'certificates': certs['ok'],
        'governance': governance['ok'],
        'verdict_schema': verdict_schema['ok'],
        'verification_schema': verification_schema['ok'],
        'refusal_schema': refusal_schema['ok'],
        'permit_schema': permit_schema['ok'],
        'compiled_backend_schema': compiled_backend_schema['ok'],
        'witness_certificate_schema': witness_certificate_schema['ok'],
        'witness_certificates': witness_certificates['ok'],
        'claim_and_tcb': claim_tcb['ok'],
        'claim_matrix': claim_matrix['ok'],
        'witness_replay': witnesses['ok'],
    }
    details = {
        'contract_version': bundle_contract.version,
        'required_files': required,
        'top_level': top_level,
        'contract': contract,
        'manifest': manifest,
        'compiler_products': compiler,
        'certificates': certs,
        'governance': governance,
        'verdict_schema': verdict_schema,
        'refusal_schema': refusal_schema,
        'permit_schema': permit_schema,
        'compiled_backend_schema': compiled_backend_schema,
        'witness_certificate_schema': witness_certificate_schema,
        'witness_certificates': witness_certificates,
        'claim_and_tcb': claim_tcb,
        'claim_matrix': claim_matrix,
        'witness_replay': witnesses,
    }
    refusal_reasons = [REFUSAL_CODE_MAP[name] for name, ok in checks.items() if not ok]
    return _verification_result(bundle_digest=manifest['bundle_digest'], overall_ok=all(checks.values()), checks=checks, details=details, refusal_reasons=refusal_reasons)
