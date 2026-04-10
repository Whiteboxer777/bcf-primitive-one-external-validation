from __future__ import annotations

import json
import shutil
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from bcf_primitive.common import canonical_bytes, digest_data, dump_json
from bcf_primitive.compiler import compile_bundle
from bcf_primitive.runtime import SealedBoundaryRunner, refuse_non_bypass
from bcf_primitive_verifier.runtime import replay_verdict
from bcf_primitive_verifier.verifier import verify_bundle
from bcf_primitive_verifier.refusal import PRIMITIVE_IDENTITY
from bcf_primitive.refusal import make_refusal
from tools.independent_second_implementation_parity import run_independent_second_implementation_parity
from tools.adversarial_closure_harness import run_adversarial_closure_harness
from tools.verification_subfamily_completion_harness import run_verification_subfamily_completion_harness
from tools.externalized_second_line_parity import run_externalized_second_line_parity


def _safe_execute(runner: SealedBoundaryRunner, request: dict[str, object], action: dict[str, object]) -> dict[str, object]:
    try:
        return runner.execute(request, action)
    except RuntimeError as exc:
        msg = str(exc)
        if msg.endswith('request_too_large'):
            return make_refusal(code='REFUSE_REQUEST_OVERSIZE', layer='runtime', bundle_digest=runner.runtime.bundle_digest, request_digest=digest_data(request), action_digest=digest_data(action), refusal_reasons=['REFUSE_REQUEST_OVERSIZE'], details={'source': 'theorem_family_corpus_harness'}) | {'overall_ok': False}
        if msg.endswith('schema_invalid'):
            return make_refusal(code='REFUSE_SCHEMA_INVALID', layer='runtime', bundle_digest=runner.runtime.bundle_digest, request_digest=digest_data(request), action_digest=digest_data(action), refusal_reasons=['REFUSE_SCHEMA_INVALID'], details={'source': 'theorem_family_corpus_harness'}) | {'overall_ok': False}
        raise


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding='utf-8'))


def _make_bundle(tmp_root: Path, profile: Path, name: str) -> Path:
    bundle = tmp_root / name
    if bundle.exists():
        shutil.rmtree(bundle)
    compile_bundle(profile, bundle)
    return bundle


def run_theorem_family_corpus_harness(project_root: str | Path, profile: str | Path) -> dict[str, object]:
    project_root = Path(project_root)
    profile = Path(profile)
    tmp_root = project_root / '.theorem_family_tmp'
    if tmp_root.exists():
        shutil.rmtree(tmp_root)
    tmp_root.mkdir(parents=True)

    allow_request = _load(project_root / 'corpus' / 'equivalence' / 'allow_request.json')
    deny_request = _load(project_root / 'corpus' / 'equivalence' / 'deny_request.json')

    family_reports: dict[str, object] = {}

    # primitive_identity
    bundle = _make_bundle(tmp_root, profile, 'primitive_identity_bundle')
    verify = verify_bundle(bundle)
    runner = SealedBoundaryRunner(bundle)
    allow = runner.execute(allow_request, {'action_id': 'tf-pi-allow', 'kind': 'emit', 'payload': {}})
    deny = runner.execute(deny_request, {'action_id': 'tf-pi-deny', 'kind': 'emit', 'payload': {}})
    family_reports['primitive_identity'] = {
        'overall_ok': verify['primitive_identity'] == allow['primitive_identity'] == deny['primitive_identity'] == PRIMITIVE_IDENTITY,
        'checks': {
            'verification_identity': verify['primitive_identity'],
            'permit_identity': allow['primitive_identity'],
            'refusal_identity': deny['primitive_identity'],
        },
    }

    # scope
    family_reports['scope'] = {
        'overall_ok': allow['action_authority']['kind'] == 'release_bound_action_descriptor' and verify['verification_result'] == 'VERIFIED',
        'checks': {
            'permit_bounded_release': allow['action_authority']['kind'],
            'verified_boundary_fitness': verify['verification_result'],
        },
    }

    # object_model
    family_reports['object_model'] = {
        'overall_ok': all(key in verify for key in ['primitive_identity', 'verification_result', 'checks', 'details', 'replay_binding']) and all(key in deny for key in ['primitive_identity', 'verdict', 'refusal_code', 'refusal_class', 'replay_binding']) and all(key in allow for key in ['primitive_identity', 'verdict', 'permit_binding', 'action_authority', 'replay_binding']),
        'checks': {
            'verification_keys_ok': True,
            'refusal_keys_ok': True,
            'permit_keys_ok': True,
        },
    }

    # canonicalization
    croot = project_root / 'corpus' / 'canonicalization'
    req_a = _load(croot / 'request_semantically_equal_a.json')
    req_b = _load(croot / 'request_semantically_equal_b.json')
    req_d = _load(croot / 'request_distinct.json')
    family_reports['canonicalization'] = {
        'overall_ok': canonical_bytes(req_a) == canonical_bytes(req_b) and digest_data(req_a) == digest_data(req_b) and canonical_bytes(req_a) != canonical_bytes(req_d),
        'checks': {
            'equal_forms_collapse': canonical_bytes(req_a) == canonical_bytes(req_b),
            'equal_digest_collapse': digest_data(req_a) == digest_data(req_b),
            'distinct_forms_remain_distinct': canonical_bytes(req_a) != canonical_bytes(req_d),
        },
    }

    # verification
    broken_required = _make_bundle(tmp_root, profile, 'verification_missing_required')
    (broken_required / 'TRUST_ROOTS.json').unlink()
    broken_extra = _make_bundle(tmp_root, profile, 'verification_extra')
    dump_json(broken_extra / 'ILLEGAL_TOP_LEVEL.json', {'illegal': True})
    family_reports['verification'] = {
        'overall_ok': verify['verification_result'] == 'VERIFIED' and verify_bundle(broken_required)['refusal_code'] == 'REFUSE_REQUIRED_FILES_MISSING' and verify_bundle(broken_extra)['refusal_code'] == 'REFUSE_UNDECLARED_FILE',
        'checks': {
            'verified_bundle': verify['verification_result'],
            'missing_required_primary_refusal': verify_bundle(broken_required)['refusal_code'],
            'undeclared_extra_primary_refusal': verify_bundle(broken_extra)['refusal_code'],
        },
    }

    # admission
    family_reports['admission'] = {
        'overall_ok': allow['verdict'] == 'ALLOW' and deny['verdict'] == 'REFUSAL',
        'checks': {
            'allow_case_verdict': allow['verdict'],
            'deny_case_verdict': deny['verdict'],
        },
    }

    # refusal
    broken_multi = _make_bundle(tmp_root, profile, 'refusal_multi')
    (broken_multi / 'TRUST_ROOTS.json').unlink()
    dump_json(broken_multi / 'ILLEGAL_TOP_LEVEL.json', {'illegal': True})
    multi_refusal = verify_bundle(broken_multi)
    family_reports['refusal'] = {
        'overall_ok': multi_refusal['refusal_code'] == 'REFUSE_REQUIRED_FILES_MISSING' and deny['refusal_code'] == 'REFUSE_VERDICT_NOT_ALLOW',
        'checks': {
            'multi_failure_primary_code': multi_refusal['refusal_code'],
            'runtime_refusal_code': deny['refusal_code'],
            'runtime_refusal_class': deny['refusal_class'],
        },
    }

    # permit
    family_reports['permit'] = {
        'overall_ok': allow['verdict'] == 'ALLOW' and allow['action_authority']['kind'] == 'release_bound_action_descriptor' and sorted(allow['permit_binding'].keys()) == ['action_digest', 'bundle_digest', 'primitive_identity', 'request_digest'],
        'checks': {
            'permit_verdict': allow['verdict'],
            'authority_kind': allow['action_authority']['kind'],
            'permit_binding_keys': sorted(allow['permit_binding'].keys()),
        },
    }

    # determinism_replay
    replay1 = replay_verdict(bundle, allow_request)
    replay2 = replay_verdict(bundle, allow_request)
    allow2 = runner.execute(allow_request, {'action_id': 'tf-det-allow2', 'kind': 'emit', 'payload': {}})
    family_reports['determinism_replay'] = {
        'overall_ok': replay1['verdict'] == replay2['verdict'] == 'ALLOW' and replay1['request_digest'] == replay2['request_digest'] and allow['bundle_digest'] == allow2['bundle_digest'] and allow['request_digest'] == allow2['request_digest'],
        'checks': {
            'replay_same_verdict': replay1['verdict'] == replay2['verdict'],
            'replay_same_request_digest': replay1['request_digest'] == replay2['request_digest'],
            'runtime_same_binding': allow['request_digest'] == allow2['request_digest'],
        },
    }

    # fail_closed
    oversize_request = {'object': {'vendor': 'ACME', 'currency': 'EUR', 'amount': 5000}, 'padding': 'X' * (70 * 1024)}
    oversize_refusal = _safe_execute(runner, oversize_request, {'action_id': 'oversize', 'kind': 'emit', 'payload': {}})
    invalid_refusal = _safe_execute(runner, 'not-a-dict', {'action_id': 'invalid', 'kind': 'emit', 'payload': {}})
    family_reports['fail_closed'] = {
        'overall_ok': verify_bundle(broken_required)['refusal_code'] == 'REFUSE_REQUIRED_FILES_MISSING' and oversize_refusal['refusal_code'] == 'REFUSE_REQUEST_OVERSIZE' and invalid_refusal['refusal_code'] == 'REFUSE_SCHEMA_INVALID',
        'checks': {
            'bundle_failure_code': verify_bundle(broken_required)['refusal_code'],
            'oversize_code': oversize_refusal['refusal_code'],
            'schema_invalid_code': invalid_refusal['refusal_code'],
        },
    }

    # no_bypass
    nb = refuse_non_bypass(bundle, allow_request, 'direct-runtime-eval')
    family_reports['no_bypass'] = {
        'overall_ok': nb['refusal_code'] == 'REFUSE_NON_BYPASS_VIOLATION',
        'checks': {'no_bypass_code': nb['refusal_code']},
    }

    # equivalence
    family_reports['equivalence'] = run_independent_second_implementation_parity(project_root, profile)

    # impossibility
    family_reports['impossibility'] = {
        'overall_ok': replay_verdict(broken_required, allow_request)['verdict'] == 'REFUSAL' and deny['permit'] is False,
        'checks': {
            'no_allow_without_verification': replay_verdict(broken_required, allow_request)['verdict'],
            'no_permit_on_deny': deny['permit'],
        },
    }

    # closure
    adversarial = run_adversarial_closure_harness(project_root, profile)
    verification_sub = run_verification_subfamily_completion_harness(project_root, profile)
    externalized = run_externalized_second_line_parity(project_root, profile)
    required_families = ['primitive_identity','scope','object_model','canonicalization','verification','admission','refusal','permit','determinism_replay','fail_closed','no_bypass','equivalence','impossibility','closure']
    required_modules = ['src/bcf_primitive/runtime.py','src/bcf_primitive_verifier/verifier.py','src/bcf_primitive_independent/runtime.py','src/bcf_primitive_independent/verifier.py','tools/adversarial_closure_harness.py']
    family_reports['closure'] = {
        'overall_ok': adversarial['overall_ok'] and all((project_root / module).exists() for module in required_modules) and all((project_root / 'corpus' / 'theorem_families' / name).exists() for name in required_families),
        'checks': {
            'required_modules_present': {module: (project_root / module).exists() for module in required_modules},
            'family_dirs_present': {name: (project_root / 'corpus' / 'theorem_families' / name).exists() for name in required_families},
            'adversarial_closure': adversarial,
        },
    }

    overall_ok = all(report['overall_ok'] for report in family_reports.values())
    out = {'overall_ok': overall_ok, 'families': family_reports}
    shutil.rmtree(tmp_root)
    return out


if __name__ == '__main__':
    print(json.dumps(run_theorem_family_corpus_harness(ROOT, ROOT / 'examples' / 'canonical' / 'invoice_profile.json'), indent=2, sort_keys=True))
