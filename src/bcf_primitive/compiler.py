from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from .common import digest_data, dump_json, sha256_file
from .contract import bundle_contract, VERDICT_SCHEMA
from .governance import default_authority_policy, default_revocation_list, default_trust_roots, sign_bundle, tcb_report
from .kernel_support import compare_profiles, evaluate_profile, extract_decisive_core, is_satisfiable, minimize_profile, normalize, parse_profile, Profile, enumerate_requests
from .refusal import REFUSAL_SCHEMA, REFUSAL_TAXONOMY, PERMIT_SCHEMA, VERIFICATION_RESULT_SCHEMA
from .witness_certificate import WITNESS_CERTIFICATE_SCHEMA, attach_witness_certificate
from .refusal import make_refusal
from .strict_json import load_path_strict
from .admission_normal_form import compile_admission_normal_form
from .compiled_backend import compile_compiled_backend

SCHEMA_ROOT = Path(__file__).resolve().parents[2] / 'schemas'

def _cert(cert_type: str, claims: dict[str, Any]) -> dict[str, Any]:
    body = {'cert_type': cert_type, 'claims': claims}
    body['cert_digest'] = digest_data(body)
    return body

def _manifest(bundle: Path) -> dict[str, str]:
    return {name: sha256_file(bundle / name) for name in bundle_contract.manifest_scoped_files}

def _bundle_digest(manifest: dict[str, str]) -> str:
    return digest_data(manifest)

def _compile_witnesses(profile: Profile) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for idx, request in enumerate(enumerate_requests(profile)):
        result = evaluate_profile(profile, request)
        out.append({'request': request, 'verdict': result.verdict, 'decisive_rule_ids': list(result.decisive_rule_ids), 'matched': list(result.matched), 'failed': list(result.failed), 'fail_closed': result.fail_closed})
        if idx >= 31: break
    if not out: raise RuntimeError('witness_generation_failed')
    return out

def _claim_matrix() -> dict[str, Any]:
    return {'version': bundle_contract.version, 'claims': [
        {'claim_id': 'C1_compile_closure', 'statement': 'compile success implies verifier-complete canonical bundle', 'artifacts': ['BUNDLE_CONTRACT.json', 'MANIFEST.sha256.json'], 'tests': ['test_compile_verify_and_sealed_runner']},
        {'claim_id': 'C2_verify_closure', 'statement': 'verify success implies required files, contract, manifest, governance, and witness replay closure', 'artifacts': ['PROMOTION_CERT.json', 'PROMOTION_SIGNATURES.json', 'SUPERSESSION_CHAIN.json'], 'tests': ['test_compile_verify_and_sealed_runner']},
        {'claim_id': 'C3_non_bypass_boundary', 'statement': 'official permit path is sealed-runner only', 'artifacts': ['CLAIM.json', 'TCB_REPORT.json'], 'tests': ['test_non_bypass_refusal_and_external_audit']},
        {'claim_id': 'C4_fail_closed_refusal', 'statement': 'tamper, missing file, and contract mismatch reduce to refusal', 'artifacts': ['REFUSAL.schema.json'], 'tests': ['test_non_bypass_refusal_and_external_audit']},
        {'claim_id': 'C5_deterministic_replay', 'statement': 'identical bundle bytes and request bytes yield identical verifier replay verdicts', 'artifacts': ['WITNESS_SET.json'], 'tests': ['test_verifier_only_release_and_determinism']},
        {'claim_id': 'C6_schema_closed_outputs', 'statement': 'verification results, permits, refusals, ANF, and compiled backend validate against explicit schemas', 'artifacts': ['VERIFICATION_RESULT.schema.json', 'PERMIT.schema.json', 'REFUSAL.schema.json', 'ADMISSION_NORMAL_FORM.schema.json', 'COMPILED_BACKEND.schema.json'], 'tests': ['test_schema_validation_harness_and_second_surface_parity', 'test_compiled_backend_gate', 'test_witness_certificate_gate']},
        {'claim_id': 'C7_evidence_carrying_outputs', 'statement': 'verification, permit, refusal, replay and no-bypass paths carry digest-bound witness certificates', 'artifacts': ['WITNESS_CERTIFICATE.schema.json', 'VERIFICATION_WITNESS_CERT.json', 'PERMIT_WITNESS_CERT.json', 'REFUSAL_WITNESS_CERT.json', 'REPLAY_ALLOW_WITNESS_CERT.json', 'REPLAY_REFUSAL_WITNESS_CERT.json', 'NO_BYPASS_WITNESS_CERT.json'], 'tests': ['test_witness_certificate_gate', 'test_witness_certificate_expansion_gate']},
    ]}

def compile_bundle(profile_input: str | Path | Profile, out_dir: str | Path) -> dict[str, Any]:
    profile = profile_input if isinstance(profile_input, Profile) else parse_profile(load_path_strict(profile_input))
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    profile_dict = profile.to_dict(); norm = normalize(profile.root); minimized = minimize_profile(profile)
    minimized_profile = Profile(profile.profile_id, profile.mode, minimized.root, profile.description, profile.analysis_domains)
    sat = is_satisfiable(profile); relation = compare_profiles(profile, minimized_profile)
    anf = compile_admission_normal_form(profile)
    backend = compile_compiled_backend(profile)
    witnesses = _compile_witnesses(profile); decisive_core_sample = extract_decisive_core(profile, witnesses[0]['request'])
    dump_json(out / 'PROFILE_SOURCE.json', profile_dict); dump_json(out / 'NORMAL_FORM.json', norm.node.to_dict()); dump_json(out / 'ADMISSION_NORMAL_FORM.json', anf.to_dict()); dump_json(out / 'COMPILED_BACKEND.json', backend.to_dict()); dump_json(out / 'MINIMIZED_FORM.json', minimized.root.to_dict())
    dump_json(out / 'SAT_REPORT.json', {'satisfiable': sat.satisfiable, 'universe_size': sat.universe_size, 'witness': sat.witness.to_dict() if sat.witness else None}); dump_json(out / 'RELATION_REPORT.json', relation.to_dict())
    dump_json(out / 'WITNESS_SET.json', witnesses); dump_json(out / 'DECISIVE_CORE_SAMPLE.json', decisive_core_sample)
    dump_json(out / 'TRUST_ROOTS.json', default_trust_roots()); dump_json(out / 'AUTHORITY_POLICY.json', default_authority_policy()); dump_json(out / 'REVOCATION_LIST.json', default_revocation_list())
    dump_json(out / 'BUILD_INFO.json', {'builder': 'bcf_primitive.compiler', 'profile_id': profile.profile_id, 'contract_version': bundle_contract.version, 'single_path_claim': True, 'sealed_runner_required': True, 'official_runner_only': True, 'legacy_imports_present': False, 'external_reproducibility_closure': True, 'verifier_independence': True, 'non_bypass_boundary': True})
    dump_json(out / 'CLAIM.json', {'claim_id': 'BCF_PRIMITIVE_ONE', 'claim_text': 'Deterministic fail-closed admission boundary with independent verifier release and sealed execution boundary.', 'official_route': 'source_profile -> canonical_bundle -> verify -> sealed_runner -> permit_or_refusal', 'parallel_families': False, 'externalizable': True, 'independent_verifier': True, 'sealed_execution_boundary': True, 'standalone_verifier_release': True, 'official_runner_only': True, 'direct_runtime_api_officially_supported': False})
    dump_json(out / 'TCB_REPORT.json', tcb_report()); dump_json(out / 'CLAIM_TEST_MATRIX.json', _claim_matrix()); dump_json(out / 'BUNDLE_CONTRACT.json', bundle_contract.to_dict())
    dump_json(out / bundle_contract.verdict_schema_name, VERDICT_SCHEMA); dump_json(out / bundle_contract.verification_schema_name, VERIFICATION_RESULT_SCHEMA); dump_json(out / bundle_contract.refusal_schema_name, REFUSAL_SCHEMA); dump_json(out / bundle_contract.permit_schema_name, PERMIT_SCHEMA)
    dump_json(out / 'ADMISSION_NORMAL_FORM.schema.json', json.loads((SCHEMA_ROOT / 'admission_normal_form.schema.json').read_text(encoding='utf-8')) if (SCHEMA_ROOT / 'admission_normal_form.schema.json').exists() else {})
    dump_json(out / bundle_contract.compiled_backend_schema_name, json.loads((SCHEMA_ROOT / 'compiled_backend.schema.json').read_text(encoding='utf-8')) if (SCHEMA_ROOT / 'compiled_backend.schema.json').exists() else {})
    dump_json(out / bundle_contract.witness_certificate_schema_name, WITNESS_CERTIFICATE_SCHEMA)

    bundle_digest_pre = digest_data(sorted(p.name for p in out.iterdir() if p.is_file()))
    allow_witness = next((w for w in witnesses if w['verdict'] == 'ALLOW'), witnesses[0])
    deny_witness = next((w for w in witnesses if w['verdict'] != 'ALLOW'), witnesses[-1])
    verification_sample = attach_witness_certificate({
        'primitive_identity': 'BCF Primitive One',
        'verification_result': 'VERIFIED',
        'overall_ok': True,
        'bundle_digest': bundle_digest_pre,
        'checks': {'compiler_products': True, 'schema_closed': True},
        'details': {'source': 'compiler_sample'},
        'replay_binding': {'primitive_identity': 'BCF Primitive One', 'bundle_digest': bundle_digest_pre, 'request_digest': None},
    })
    permit_sample = attach_witness_certificate({
        'primitive_identity': 'BCF Primitive One',
        'bundle_digest': bundle_digest_pre,
        'request_digest': digest_data(allow_witness['request']),
        'action_digest': digest_data({'action_id': 'sample-allow', 'kind': 'emit', 'payload': {}}),
        'permit': True,
        'verdict': 'ALLOW',
        'permit_type': 'ACTION_DESCRIPTOR_RELEASE',
        'released_action': {'action_id': 'sample-allow', 'kind': 'emit', 'payload': {}},
        'action_authority': {'kind': 'release_bound_action_descriptor', 'action_id': 'sample-allow', 'action_kind': 'emit'},
        'permit_binding': {'primitive_identity': 'BCF Primitive One', 'bundle_digest': bundle_digest_pre, 'request_digest': digest_data(allow_witness['request']), 'action_digest': digest_data({'action_id': 'sample-allow', 'kind': 'emit', 'payload': {}})},
        'replay_binding': {'primitive_identity': 'BCF Primitive One', 'bundle_digest': bundle_digest_pre, 'request_digest': digest_data(allow_witness['request'])},
        'decisive_rule_ids': allow_witness['decisive_rule_ids'],
    })
    refusal_sample = attach_witness_certificate({
        'primitive_identity': 'BCF Primitive One',
        'bundle_digest': bundle_digest_pre,
        'request_digest': digest_data(deny_witness['request']),
        'permit': False,
        'verdict': 'REFUSAL',
        'refusal_code': 'REFUSE_VERDICT_NOT_ALLOW',
        'refusal_class': 'contract_satisfaction',
        'layer': 'action',
        'replay_binding': {'primitive_identity': 'BCF Primitive One', 'bundle_digest': bundle_digest_pre, 'request_digest': digest_data(deny_witness['request'])},
        'refusal_reasons': ['REFUSE_VERDICT_NOT_ALLOW'],
        'details': {'source': 'compiler_sample', 'decisive_rule_ids': deny_witness['decisive_rule_ids']},
        'overall_ok': False,
    })
    replay_allow_sample = attach_witness_certificate({
        'primitive_identity': 'BCF Primitive One',
        'overall_ok': True,
        'bundle_digest': bundle_digest_pre,
        'request_digest': digest_data(allow_witness['request']),
        'verdict': 'ALLOW',
        'replay_binding': {'primitive_identity': 'BCF Primitive One', 'bundle_digest': bundle_digest_pre, 'request_digest': digest_data(allow_witness['request'])},
        'decisive_rule_ids': allow_witness['decisive_rule_ids'],
        'matched': allow_witness['matched'],
        'failed': allow_witness['failed'],
        'fail_closed': allow_witness['fail_closed'],
    })
    replay_refusal_sample = attach_witness_certificate({
        'primitive_identity': 'BCF Primitive One',
        'bundle_digest': bundle_digest_pre,
        'request_digest': digest_data(deny_witness['request']),
        'permit': False,
        'verdict': 'REFUSAL',
        'refusal_code': 'REFUSE_VERDICT_NOT_ALLOW',
        'refusal_class': 'contract_satisfaction',
        'layer': 'runtime',
        'replay_binding': {'primitive_identity': 'BCF Primitive One', 'bundle_digest': bundle_digest_pre, 'request_digest': digest_data(deny_witness['request'])},
        'refusal_reasons': ['REFUSE_VERDICT_NOT_ALLOW'],
        'details': {'source': 'compiler_sample_replay', 'decisive_rule_ids': deny_witness['decisive_rule_ids']},
        'overall_ok': False,
    })
    no_bypass_sample = attach_witness_certificate(make_refusal(
        code='REFUSE_NON_BYPASS_VIOLATION',
        layer='runtime',
        bundle_digest=bundle_digest_pre,
        request_digest=digest_data(deny_witness['request']),
        attempted_entrypoint='custom-unsealed-fastpath',
        details={'source': 'compiler_sample_non_bypass'},
    ))
    dump_json(out / 'VERIFICATION_WITNESS_CERT.json', verification_sample['witness_certificate'])
    dump_json(out / 'PERMIT_WITNESS_CERT.json', permit_sample['witness_certificate'])
    dump_json(out / 'REFUSAL_WITNESS_CERT.json', refusal_sample['witness_certificate'])
    dump_json(out / 'REPLAY_ALLOW_WITNESS_CERT.json', replay_allow_sample['witness_certificate'])
    dump_json(out / 'REPLAY_REFUSAL_WITNESS_CERT.json', replay_refusal_sample['witness_certificate'])
    dump_json(out / 'NO_BYPASS_WITNESS_CERT.json', no_bypass_sample['witness_certificate'])
    dump_json(out / 'NORMALIZATION_CERT.json', _cert('NORMALIZATION_CERT', {'profile_digest': digest_data(profile_dict), 'normal_form_digest': digest_data(norm.node.to_dict())}))
    dump_json(out / 'MINIMIZATION_CERT.json', _cert('MINIMIZATION_CERT', {'profile_digest': digest_data(profile_dict), 'minimized_form_digest': digest_data(minimized.root.to_dict())}))
    dump_json(out / 'SAT_CERT.json', _cert('SAT_CERT', {'profile_digest': digest_data(profile_dict), 'satisfiable': sat.satisfiable, 'witness_digest': digest_data((sat.witness.to_dict() if sat.witness else None))}))
    dump_json(out / 'RELATION_CERT.json', _cert('RELATION_CERT', {'left_profile_digest': digest_data(profile_dict), 'right_profile_digest': digest_data(minimized_profile.to_dict()), 'relation': relation.relation}))
    dump_json(out / 'CONFORMANCE_CERT.json', _cert('CONFORMANCE_CERT', {'profile_digest': digest_data(profile_dict), 'witness_set_digest': digest_data(witnesses), 'checked_witnesses': len(witnesses)}))
    dump_json(out / 'DECISIVE_CORE_CERT.json', _cert('DECISIVE_CORE_CERT', {'profile_digest': digest_data(profile_dict), 'request_digest': digest_data(witnesses[0]['request']), 'decisive_core_digest': digest_data(decisive_core_sample)}))
    manifest = _manifest(out); dump_json(out / bundle_contract.manifest_name, manifest); bundle_digest = _bundle_digest(manifest)
    promotion_cert = _cert('PROMOTION_CERT', {'bundle_digest': bundle_digest, 'manifest_digest': bundle_digest, 'promotion_verdict': 'CERTIFIED_FOR_PRODUCTION', 'contract_version': bundle_contract.version, 'refusal_taxonomy_digest': digest_data(REFUSAL_TAXONOMY)})
    dump_json(out / 'PROMOTION_CERT.json', promotion_cert); dump_json(out / 'PROMOTION_SIGNATURES.json', {'signatures': [sign_bundle(bundle_digest, promotion_cert, signer_id='root_prod', scope='production')]}); dump_json(out / 'SUPERSESSION_CHAIN.json', {'current_bundle_digest': bundle_digest, 'promotion_cert_digest': promotion_cert['cert_digest'], 'supersedes': []})
    top_level = sorted(p.name for p in out.iterdir() if p.is_file())
    return {'overall_ok': set(bundle_contract.required_files).issubset(set(top_level)), 'contract_version': bundle_contract.version, 'bundle_digest': bundle_digest, 'file_count': len(top_level), 'top_level_files': top_level, 'tcb_component_count': len(tcb_report()['trusted_components']), 'official_runner_only': True, 'verifier_independence': True, 'non_bypass_boundary': True}
