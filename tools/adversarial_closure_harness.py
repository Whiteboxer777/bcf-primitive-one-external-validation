from __future__ import annotations

import json
import shutil
from copy import deepcopy
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from bcf_primitive.common import canonical_bytes, digest_data, dump_json, load_json, sha256_file
from bcf_primitive.contract import bundle_contract
from bcf_primitive.governance import sign_bundle
from bcf_primitive.refusal import REFUSAL_TAXONOMY
from bcf_primitive.compiler import compile_bundle
from bcf_primitive.runtime import SealedBoundaryRunner, refuse_non_bypass
from bcf_primitive_verifier.runtime import replay_verdict
from bcf_primitive_verifier.verifier import verify_bundle
from bcf_primitive_independent.runtime import IndependentRunner, replay_verdict_independent
from bcf_primitive_independent.verifier import verify_bundle_independent
from tools.schema_validation_harness import _validate
from tools.independent_second_implementation_parity import _normalize
from bcf_primitive_verifier.refusal import PERMIT_SCHEMA, REFUSAL_SCHEMA, VERIFICATION_RESULT_SCHEMA


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def _mutate_json_file(path: Path, patch: dict[str, Any], patch_index: int | None = None) -> None:
    payload = _load_json(path)
    if patch_index is not None:
        assert isinstance(payload, list)
        target = payload[patch_index]
    else:
        target = payload
    for dotted, value in patch.items():
        cur = target
        parts = dotted.split('.')
        for part in parts[:-1]:
            if part not in cur or not isinstance(cur[part], dict):
                cur[part] = {}
            cur = cur[part]
        cur[parts[-1]] = value
    dump_json(path, payload)


def _make_bundle(tmp_root: Path, profile: Path, name: str) -> Path:
    bundle = tmp_root / name
    if bundle.exists():
        shutil.rmtree(bundle)
    compile_bundle(profile, bundle)
    return bundle




def _sync_manifest_and_governance(bundle: Path) -> None:
    manifest_path = bundle / 'MANIFEST.sha256.json'
    manifest = load_json(manifest_path)
    for rel in bundle_contract.manifest_scoped_files:
        target = bundle / rel
        if target.exists():
            manifest[rel] = sha256_file(target)
    dump_json(manifest_path, manifest)
    bundle_digest = digest_data(manifest)
    claims = {
        'bundle_digest': bundle_digest,
        'manifest_digest': bundle_digest,
        'promotion_verdict': 'CERTIFIED_FOR_PRODUCTION',
        'contract_version': bundle_contract.version,
        'refusal_taxonomy_digest': digest_data(REFUSAL_TAXONOMY),
    }
    promotion_cert = {'cert_type': 'PROMOTION_CERT', 'claims': claims}
    promotion_cert['cert_digest'] = digest_data(promotion_cert)
    dump_json(bundle / 'PROMOTION_CERT.json', promotion_cert)
    dump_json(bundle / 'PROMOTION_SIGNATURES.json', {'signatures': [sign_bundle(bundle_digest, promotion_cert, signer_id='root_prod', scope='production')]})
    dump_json(bundle / 'SUPERSESSION_CHAIN.json', {'current_bundle_digest': bundle_digest, 'promotion_cert_digest': promotion_cert['cert_digest'], 'supersedes': []})

def _apply_mutation(bundle: Path, case: dict[str, Any]) -> None:
    mutation = case['mutation']
    if mutation == 'remove_file':
        (bundle / case['target']).unlink()
        return
    if mutation == 'add_file':
        dump_json(bundle / case['target'], case.get('payload', {}))
        return
    if mutation == 'json_patch':
        _mutate_json_file(bundle / case['target'], case['patch'], case.get('patch_index'))
        if case.get('sync_manifest'):
            _sync_manifest_and_governance(bundle)
        return
    if mutation == 'remove_and_add':
        (bundle / case['remove']).unlink()
        dump_json(bundle / case['add'], case.get('payload', {}))
        return
    if mutation == 'contract_and_manifest':
        _mutate_json_file(bundle / 'BUNDLE_CONTRACT.json', {'semantics.official_runner': 'broken-fastpath'})
        _mutate_json_file(bundle / 'MANIFEST.sha256.json', {'PROFILE_SOURCE.json': '1' * 64})
        return
    raise ValueError(f'unsupported mutation: {mutation}')


def _safe_execute(runner: SealedBoundaryRunner, request: Any, action: Any) -> dict[str, Any]:
    try:
        return runner.execute(request, action)
    except RuntimeError as exc:
        msg = str(exc)
        if msg.endswith('request_too_large'):
            from bcf_primitive.refusal import make_refusal
            return make_refusal(code='REFUSE_REQUEST_OVERSIZE', layer='runtime', bundle_digest=runner.runtime.bundle_digest, request_digest=digest_data(request), action_digest=digest_data(action) if isinstance(action, dict) else None, refusal_reasons=['REFUSE_REQUEST_OVERSIZE'], details={'source': 'adversarial_closure_harness'}) | {'overall_ok': False}
        if msg.endswith('schema_invalid'):
            from bcf_primitive.refusal import make_refusal
            return make_refusal(code='REFUSE_SCHEMA_INVALID', layer='runtime', bundle_digest=runner.runtime.bundle_digest, request_digest=digest_data(request), action_digest=digest_data(action) if isinstance(action, dict) else None, refusal_reasons=['REFUSE_SCHEMA_INVALID'], details={'source': 'adversarial_closure_harness'}) | {'overall_ok': False}
        if msg.endswith('action_descriptor_invalid'):
            from bcf_primitive.refusal import make_refusal
            return make_refusal(code='REFUSE_ACTION_DESCRIPTOR_INVALID', layer='action', bundle_digest=runner.runtime.bundle_digest, request_digest=digest_data(request), action_digest=digest_data(action) if isinstance(action, dict) else None, refusal_reasons=['REFUSE_ACTION_DESCRIPTOR_INVALID'], details={'source': 'adversarial_closure_harness'}) | {'overall_ok': False}
        raise


def _run_verification_family(project_root: Path, profile: Path, tmp_root: Path) -> dict[str, Any]:
    corpus = _load_json(project_root / 'corpus' / 'adversarial' / 'verification' / 'cases.json')['cases']
    case_reports: dict[str, Any] = {}
    overall_ok = True
    for case in corpus:
        bundle = _make_bundle(tmp_root, profile, case['case_id'])
        _apply_mutation(bundle, case)
        primary = verify_bundle(bundle)
        independent = verify_bundle_independent(bundle)
        ok = (
            primary.get('verification_result') == case['expected_verification']
            and primary.get('refusal_code') == case['expected_refusal_code']
            and primary.get('refusal_class') == case['expected_refusal_class']
            and independent.get('refusal_code') == case['expected_refusal_code']
            and independent.get('refusal_class') == case['expected_refusal_class']
            and _validate(REFUSAL_SCHEMA, primary)['ok']
            and _validate(REFUSAL_SCHEMA, independent)['ok']
        )
        overall_ok = overall_ok and ok
        case_reports[case['case_id']] = {'ok': ok, 'primary': _normalize(primary), 'independent': _normalize(independent), 'expected': case}
    return {'overall_ok': overall_ok, 'cases': case_reports}


def _run_admission_family(project_root: Path, profile: Path, tmp_root: Path) -> dict[str, Any]:
    corpus_dir = project_root / 'corpus' / 'adversarial' / 'admission'
    cases = _load_json(corpus_dir / 'cases.json')['cases']
    bundle = _make_bundle(tmp_root, profile, 'admission_family')
    primary_runner = SealedBoundaryRunner(bundle)
    independent_runner = IndependentRunner(bundle)
    case_reports: dict[str, Any] = {}
    overall_ok = True
    for case in cases:
        request = _load_json(corpus_dir / case['request_file'])
        action = _load_json(corpus_dir / case['action_file'])
        primary = _safe_execute(primary_runner, request, action)
        independent = independent_runner.execute(request, action)
        if case['expected_verdict'] == 'ALLOW':
            ok = primary.get('verdict') == independent.get('verdict') == 'ALLOW' and _validate(PERMIT_SCHEMA, primary)['ok'] and _validate(PERMIT_SCHEMA, independent)['ok']
        else:
            ok = primary.get('verdict') == independent.get('verdict') == 'REFUSAL' and primary.get('refusal_code') == independent.get('refusal_code') == case['expected_refusal_code'] and _validate(REFUSAL_SCHEMA, primary)['ok'] and _validate(REFUSAL_SCHEMA, independent)['ok']
        overall_ok = overall_ok and ok
        case_reports[case['case_id']] = {'ok': ok, 'primary': _normalize(primary), 'independent': _normalize(independent), 'expected': case}
    return {'overall_ok': overall_ok, 'cases': case_reports}


def _run_refusal_precedence_family(project_root: Path, profile: Path, tmp_root: Path) -> dict[str, Any]:
    corpus_dir = project_root / 'corpus' / 'adversarial' / 'refusal_precedence'
    cases = _load_json(corpus_dir / 'cases.json')['cases']
    case_reports: dict[str, Any] = {}
    overall_ok = True
    for case in cases:
        if case['kind'] == 'bundle_mutation':
            bundle = _make_bundle(tmp_root, profile, case['case_id'])
            _apply_mutation(bundle, case)
            primary = verify_bundle(bundle)
            independent = verify_bundle_independent(bundle)
        else:
            bundle = _make_bundle(tmp_root, profile, case['case_id'])
            runner = SealedBoundaryRunner(bundle)
            indep = IndependentRunner(bundle)
            request = _load_json(project_root / 'corpus' / 'adversarial' / 'admission' / case['request_file'])
            action = _load_json(project_root / 'corpus' / 'adversarial' / 'admission' / case['action_file'])
            primary = _safe_execute(runner, request, action)
            independent = indep.execute(request, action)
        ok = primary.get('refusal_code') == independent.get('refusal_code') == case['expected_refusal_code'] and primary.get('refusal_class') == independent.get('refusal_class') == case['expected_refusal_class']
        overall_ok = overall_ok and ok
        case_reports[case['case_id']] = {'ok': ok, 'primary': _normalize(primary), 'independent': _normalize(independent), 'expected': case}
    return {'overall_ok': overall_ok, 'cases': case_reports}


def _run_permit_family(project_root: Path, profile: Path, tmp_root: Path) -> dict[str, Any]:
    corpus_dir = project_root / 'corpus' / 'adversarial' / 'permit_boundedness'
    cases = _load_json(corpus_dir / 'cases.json')['cases']
    bundle = _make_bundle(tmp_root, profile, 'permit_family')
    runner = SealedBoundaryRunner(bundle)
    indep = IndependentRunner(bundle)
    case_reports: dict[str, Any] = {}
    overall_ok = True
    for case in cases:
        request = _load_json(corpus_dir / case['request_file'])
        action = _load_json(corpus_dir / case['action_file'])
        primary = _safe_execute(runner, request, action)
        independent = indep.execute(request, action)
        if case['kind'] == 'permit_scope_probe':
            forbidden = case['forbid_extra_authority_keys']
            ok = all(k not in primary.get('action_authority', {}) for k in forbidden) and all(k not in independent.get('action_authority', {}) for k in forbidden)
        else:
            ok = (
                primary.get('verdict') == independent.get('verdict') == case['expected_verdict'] == 'ALLOW'
                and primary.get('action_authority', {}).get('kind') == independent.get('action_authority', {}).get('kind') == case['expected_authority_kind']
                and primary.get('permit_binding', {}).get('bundle_digest') == independent.get('permit_binding', {}).get('bundle_digest')
                and _validate(PERMIT_SCHEMA, primary)['ok']
                and _validate(PERMIT_SCHEMA, independent)['ok']
            )
        overall_ok = overall_ok and ok
        case_reports[case['case_id']] = {'ok': ok, 'primary': _normalize(primary), 'independent': _normalize(independent), 'expected': case}
    return {'overall_ok': overall_ok, 'cases': case_reports}


def _run_canonicalization_family(project_root: Path) -> dict[str, Any]:
    corpus_dir = project_root / 'corpus' / 'adversarial' / 'canonicalization'
    cases = _load_json(corpus_dir / 'cases.json')['cases']
    case_reports: dict[str, Any] = {}
    overall_ok = True
    for case in cases:
        if case['kind'] == 'canonical_pair':
            left = _load_json(corpus_dir / case['left'])
            right = _load_json(corpus_dir / case['right'])
            equal = canonical_bytes(left) == canonical_bytes(right) and digest_data(left) == digest_data(right)
            ok = equal is case['expected_equal']
            case_reports[case['case_id']] = {'ok': ok, 'left_digest': digest_data(left), 'right_digest': digest_data(right), 'expected_equal': case['expected_equal']}
        else:
            target = _load_json(corpus_dir / case['target'])
            first = canonical_bytes(target)
            second = canonical_bytes(json.loads(first.decode('utf-8')))
            ok = first == second if case['expected_stable'] else first != second
            case_reports[case['case_id']] = {'ok': ok, 'digest': digest_data(target), 'expected_stable': case['expected_stable']}
        overall_ok = overall_ok and case_reports[case['case_id']]['ok']
    return {'overall_ok': overall_ok, 'cases': case_reports}


def _run_no_bypass_family(project_root: Path, profile: Path, tmp_root: Path) -> dict[str, Any]:
    corpus_dir = project_root / 'corpus' / 'adversarial' / 'no_bypass'
    cases = _load_json(corpus_dir / 'cases.json')['cases']
    bundle = _make_bundle(tmp_root, profile, 'no_bypass_family')
    case_reports: dict[str, Any] = {}
    overall_ok = True
    for case in cases:
        request = _load_json(corpus_dir / case['request_file'])
        refusal = refuse_non_bypass(bundle, request, case['entrypoint'])
        ok = refusal.get('refusal_code') == case['expected_refusal_code'] and _validate(REFUSAL_SCHEMA, refusal)['ok']
        overall_ok = overall_ok and ok
        case_reports[case['case_id']] = {'ok': ok, 'refusal': _normalize(refusal), 'expected': case}
    return {'overall_ok': overall_ok, 'cases': case_reports}


def _run_equivalence_family(project_root: Path, profile: Path, tmp_root: Path) -> dict[str, Any]:
    corpus_dir = project_root / 'corpus' / 'adversarial' / 'equivalence'
    verification_cases = {c['case_id']: c for c in _load_json(project_root / 'corpus' / 'adversarial' / 'verification' / 'cases.json')['cases']}
    cases = _load_json(corpus_dir / 'cases.json')['cases']
    case_reports: dict[str, Any] = {}
    overall_ok = True
    for case in cases:
        if case['kind'] == 'verify_mutation':
            bundle = _make_bundle(tmp_root, profile, case['case_id'])
            ref = verification_cases[case['mutation_ref']]
            _apply_mutation(bundle, ref)
            primary = verify_bundle(bundle)
            independent = verify_bundle_independent(bundle)
        else:
            bundle = _make_bundle(tmp_root, profile, case['case_id'])
            request = _load_json(corpus_dir / case['request_file'])
            action = _load_json(corpus_dir / case['action_file'])
            primary = _normalize(_safe_execute(SealedBoundaryRunner(bundle), request, action))
            independent = _normalize(IndependentRunner(bundle).execute(request, action))
            ok = primary['decision_class'] == independent['decision_class'] == case['expected_verdict'] and primary.get('refusal_code') == independent.get('refusal_code') == case.get('expected_refusal_code')
            overall_ok = overall_ok and ok
            case_reports[case['case_id']] = {'ok': ok, 'primary': primary, 'independent': independent, 'expected': case}
            continue
        pnorm = _normalize(primary)
        inorm = _normalize(independent)
        ok = pnorm['decision_class'] == inorm['decision_class'] == 'NOT_VERIFIED' and pnorm['refusal_code'] == inorm['refusal_code'] == case['expected_refusal_code']
        overall_ok = overall_ok and ok
        case_reports[case['case_id']] = {'ok': ok, 'primary': pnorm, 'independent': inorm, 'expected': case}
    return {'overall_ok': overall_ok, 'cases': case_reports}


def run_adversarial_closure_harness(project_root: str | Path, profile: str | Path) -> dict[str, Any]:
    project_root = Path(project_root)
    profile = Path(profile)
    tmp_root = project_root / '.adversarial_closure_tmp'
    if tmp_root.exists():
        shutil.rmtree(tmp_root)
    tmp_root.mkdir(parents=True)
    try:
        families = {
            'verification': _run_verification_family(project_root, profile, tmp_root),
            'admission': _run_admission_family(project_root, profile, tmp_root),
            'refusal_precedence': _run_refusal_precedence_family(project_root, profile, tmp_root),
            'permit_boundedness': _run_permit_family(project_root, profile, tmp_root),
            'canonicalization': _run_canonicalization_family(project_root),
            'no_bypass': _run_no_bypass_family(project_root, profile, tmp_root),
            'equivalence': _run_equivalence_family(project_root, profile, tmp_root),
        }
        overall_ok = all(report['overall_ok'] for report in families.values())
        return {'overall_ok': overall_ok, 'families': families, 'target_name': 'adversarial_closure_pass'}
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)


if __name__ == '__main__':
    print(json.dumps(run_adversarial_closure_harness(ROOT, ROOT / 'examples' / 'canonical' / 'invoice_profile.json'), indent=2, sort_keys=True))
