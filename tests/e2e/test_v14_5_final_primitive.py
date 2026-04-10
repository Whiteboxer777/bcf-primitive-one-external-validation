from pathlib import Path
import json
from bcf_primitive.capsule import build_standalone_verifier_release
from bcf_primitive.compiler import compile_bundle
from bcf_primitive.runtime import SealedBoundaryRunner, refuse_non_bypass
from bcf_primitive_verifier.runtime import replay_verdict
from bcf_primitive_verifier.verifier import verify_bundle
from bcf_primitive_verifier.refusal import PRIMITIVE_IDENTITY, REFUSAL_SCHEMA, PERMIT_SCHEMA
from tools.audit_bundle import run_external_audit
from tools.equivalence_harness import run_equivalence_harness
from tools.schema_validation_harness import run_schema_validation_harness
from tools.second_surface_parity_target import run_second_surface_parity_target
from tools.independent_second_implementation_parity import run_independent_second_implementation_parity
from tools.theorem_family_corpus_harness import run_theorem_family_corpus_harness
from tools.adversarial_closure_harness import run_adversarial_closure_harness
from tools.verification_subfamily_completion_harness import run_verification_subfamily_completion_harness
from tools.externalized_second_line_parity import run_externalized_second_line_parity
from tools.node_out_of_family_parity import run_node_out_of_family_parity
from tools.node_verification_subfamily_parity import run_node_verification_subfamily_parity
from tools.theorem_discharge_ledger import build_theorem_discharge_ledger, emit_theorem_discharge_markdown
EXAMPLES = Path('examples/canonical')

def test_compile_verify_and_sealed_runner(tmp_path: Path):
    bundle = tmp_path / 'bundle'
    compile_report = compile_bundle(EXAMPLES / 'invoice_profile.json', bundle)
    assert compile_report['overall_ok'] is True
    verify_report = verify_bundle(bundle)
    assert verify_report['overall_ok'] is True
    assert verify_report['verification_result'] == 'VERIFIED'
    runner = SealedBoundaryRunner(bundle)
    allow_req = {'object': {'vendor': 'ACME', 'currency': 'EUR', 'amount': 5000}}
    deny_req = {'object': {'vendor': 'ACME', 'currency': 'EUR', 'amount': 11000}}
    allow_result = runner.execute(allow_req, {'action_id': '1', 'kind': 'emit', 'payload': {}})
    deny_result = runner.execute(deny_req, {'action_id': '2', 'kind': 'emit', 'payload': {}})
    assert allow_result['permit'] is True
    assert allow_result['primitive_identity'] == PRIMITIVE_IDENTITY
    assert allow_result['verdict'] == 'ALLOW'
    assert allow_result['permit_binding']['primitive_identity'] == PRIMITIVE_IDENTITY
    assert allow_result['action_authority']['kind'] == 'release_bound_action_descriptor'
    assert deny_result['permit'] is False
    assert deny_result['refusal_code'] == 'REFUSE_VERDICT_NOT_ALLOW'
    assert deny_result['refusal_class'] == 'contract_satisfaction'

def test_non_bypass_refusal_and_external_audit(tmp_path: Path):
    bundle = tmp_path / 'bundle'
    compile_bundle(EXAMPLES / 'invoice_profile.json', bundle)
    refusal = refuse_non_bypass(bundle, {'object': {'vendor': 'ACME', 'currency': 'EUR', 'amount': 5000}}, 'direct-runtime-eval')
    assert refusal['refusal_code'] == 'REFUSE_NON_BYPASS_VIOLATION'
    assert refusal['refusal_class'] == 'non_bypass'
    audit = run_external_audit(EXAMPLES / 'invoice_profile.json', EXAMPLES / 'invoice_request_allow.json', EXAMPLES / 'invoice_deny_request.json')
    assert audit['overall_ok'] is True

def test_verifier_negative_normalized_refusal_object_and_permit_schema(tmp_path: Path):
    bundle = tmp_path / 'bundle'
    compile_bundle(EXAMPLES / 'invoice_profile.json', bundle)
    (bundle / 'TRUST_ROOTS.json').unlink()
    verify_report = verify_bundle(bundle)
    assert verify_report['overall_ok'] is False
    assert verify_report['verdict'] == 'REFUSAL'
    assert verify_report['verification_result'] == 'NOT_VERIFIED'
    assert verify_report['primitive_identity'] == PRIMITIVE_IDENTITY
    assert verify_report['refusal_code'] == 'REFUSE_REQUIRED_FILES_MISSING'
    assert 'REFUSE_REQUIRED_FILES_MISSING' in verify_report['refusal_reasons']
    permit_schema = json.loads((Path('schemas') / 'permit.schema.json').read_text(encoding='utf-8'))
    refusal_schema = json.loads((Path('schemas') / 'refusal.schema.json').read_text(encoding='utf-8'))
    assert 'permit_binding' in permit_schema['required']
    assert refusal_schema['properties']['verdict']['enum'] == ['REFUSAL']

def test_verifier_only_release_and_determinism_and_equivalence(tmp_path: Path):
    bundle = tmp_path / 'bundle'
    compile_bundle(EXAMPLES / 'invoice_profile.json', bundle)
    release_zip = tmp_path / 'verifier.zip'
    report = build_standalone_verifier_release(Path('.'), release_zip)
    assert report['overall_ok'] is True
    request = {'object': {'vendor': 'ACME', 'currency': 'EUR', 'amount': 5000}}
    r1 = replay_verdict(bundle, request)
    r2 = replay_verdict(bundle, request)
    assert r1['overall_ok'] is True and r2['overall_ok'] is True
    assert r1['verdict'] == r2['verdict'] == 'ALLOW'
    assert r1['request_digest'] == r2['request_digest']
    eq = run_equivalence_harness(Path('.'), EXAMPLES / 'invoice_profile.json')
    assert eq['overall_ok'] is True


def test_schema_validation_harness_and_second_surface_parity(tmp_path: Path):
    schema_report = run_schema_validation_harness(Path('.'), EXAMPLES / 'invoice_profile.json')
    assert schema_report['overall_ok'] is True
    assert schema_report['verification']['schema_validation']['ok'] is True
    assert schema_report['permit']['schema_validation']['ok'] is True
    assert schema_report['refusal']['schema_validation']['ok'] is True
    assert schema_report['replay_refusal']['schema_validation']['ok'] is True
    second_surface = run_second_surface_parity_target(Path('.'), EXAMPLES / 'invoice_profile.json')
    assert second_surface['overall_ok'] is True
    assert second_surface['cases']['allow_case']['parity_ok'] is True
    assert second_surface['cases']['deny_case']['parity_ok'] is True


def test_bundle_contains_verification_schema_and_contract_names(tmp_path: Path):
    bundle = tmp_path / 'bundle'
    compile_bundle(EXAMPLES / 'invoice_profile.json', bundle)
    contract = json.loads((bundle / 'BUNDLE_CONTRACT.json').read_text(encoding='utf-8'))
    assert contract['verification_schema_name'] == 'VERIFICATION_RESULT.schema.json'
    assert (bundle / 'VERIFICATION_RESULT.schema.json').exists()


def test_independent_second_implementation_parity_and_theorem_family_corpus():
    parity = run_independent_second_implementation_parity(Path('.'), EXAMPLES / 'invoice_profile.json')
    assert parity['overall_ok'] is True
    assert parity['cases']['verify']['parity_ok'] is True
    assert parity['cases']['allow_runtime']['parity_ok'] is True
    assert parity['cases']['deny_runtime']['parity_ok'] is True
    theorem_report = run_theorem_family_corpus_harness(Path('.'), EXAMPLES / 'invoice_profile.json')
    assert theorem_report['overall_ok'] is True
    for family_name, family_report in theorem_report['families'].items():
        assert family_report['overall_ok'] is True, family_name


def test_adversarial_closure_harness_and_saturated_equivalence():
    adversarial = run_adversarial_closure_harness(Path('.'), EXAMPLES / 'invoice_profile.json')
    assert adversarial['overall_ok'] is True
    assert adversarial['families']['verification']['overall_ok'] is True
    assert adversarial['families']['admission']['overall_ok'] is True
    assert adversarial['families']['refusal_precedence']['overall_ok'] is True
    assert adversarial['families']['permit_boundedness']['overall_ok'] is True
    assert adversarial['families']['canonicalization']['overall_ok'] is True
    assert adversarial['families']['no_bypass']['overall_ok'] is True
    assert adversarial['families']['equivalence']['overall_ok'] is True
    eq = run_equivalence_harness(Path('.'), EXAMPLES / 'invoice_profile.json')
    assert eq['adversarial_closure']['overall_ok'] is True


def test_verification_subfamily_completion_and_externalized_second_line_parity():
    verification_sub = run_verification_subfamily_completion_harness(Path('.'), EXAMPLES / 'invoice_profile.json')
    assert verification_sub['overall_ok'] is True
    for family_name, family_report in verification_sub['families'].items():
        assert family_report['overall_ok'] is True, family_name
    externalized = run_externalized_second_line_parity(Path('.'), EXAMPLES / 'invoice_profile.json')
    assert externalized['overall_ok'] is True
    for case_name, case_report in externalized['cases'].items():
        assert case_report['parity_ok'] is True, case_name


def test_node_out_of_family_second_line_and_theorem_discharge_ledger(tmp_path: Path):
    node_parity = run_node_out_of_family_parity(Path('.'), EXAMPLES / 'invoice_profile.json')
    assert node_parity['overall_ok'] is True
    for case_name, case_report in node_parity['cases'].items():
        assert case_report['parity_ok'] is True, case_name
    node_vf = run_node_verification_subfamily_parity(Path('.'), EXAMPLES / 'invoice_profile.json')
    assert node_vf['overall_ok'] is True
    for family_name, family_report in node_vf['families'].items():
        assert family_report['overall_ok'] is True, family_name
    # Materialize the report inputs the discharge ledger expects.
    from tools.equivalence_harness import run_equivalence_harness
    eq = run_equivalence_harness(Path('.'), EXAMPLES / 'invoice_profile.json')
    (Path('dist') / 'node_out_of_family_parity_report.json').write_text(json.dumps(node_parity, indent=2, sort_keys=True), encoding='utf-8')
    (Path('dist') / 'node_verification_subfamily_parity_report.json').write_text(json.dumps(node_vf, indent=2, sort_keys=True), encoding='utf-8')
    (Path('dist') / 'equivalence_report.json').write_text(json.dumps(eq, indent=2, sort_keys=True), encoding='utf-8')
    (Path('REPORTS') / 'node_out_of_family_parity_report.json').write_text(json.dumps(node_parity, indent=2, sort_keys=True), encoding='utf-8')
    (Path('REPORTS') / 'node_verification_subfamily_parity_report.json').write_text(json.dumps(node_vf, indent=2, sort_keys=True), encoding='utf-8')
    ledger = build_theorem_discharge_ledger(Path('.'))
    assert ledger['summary']['node_out_of_family_parity'] is True
    assert ledger['summary']['node_verification_subfamily_parity'] is True
    md = emit_theorem_discharge_markdown(ledger)
    assert 'THEOREM_DISCHARGE_LEDGER' in md
    assert 'node_out_of_family_parity' in md
