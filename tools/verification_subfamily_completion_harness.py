from __future__ import annotations

import json
import shutil
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SRC = ROOT / 'src'
EXT_SRC = ROOT / 'externalized_second_line' / 'src'
for p in (SRC, EXT_SRC):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from bcf_primitive.compiler import compile_bundle
from bcf_primitive.common import dump_json, load_json, sha256_file
from bcf_primitive.contract import bundle_contract
from bcf_primitive.governance import sign_bundle
from bcf_primitive.refusal import REFUSAL_TAXONOMY
from bcf_primitive_verifier.verifier import verify_bundle
from bcf_primitive_independent.verifier import verify_bundle_independent
from bcf_primitive_externalized.verifier import verify_bundle_externalized
from bcf_primitive_verifier.refusal import REFUSAL_SCHEMA
from tools.schema_validation_harness import _validate
from tools.independent_second_implementation_parity import _normalize


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
        parts = dotted.split('.')
        cur = target
        for part in parts[:-1]:
            if isinstance(cur, list):
                cur = cur[int(part)]
            else:
                if part not in cur or not isinstance(cur[part], (dict, list)):
                    cur[part] = {}
                cur = cur[part]
        last = parts[-1]
        if isinstance(cur, list):
            cur[int(last)] = value
        else:
            cur[last] = value
    dump_json(path, payload)


def _sync_manifest_and_governance(bundle: Path) -> None:
    manifest_path = bundle / 'MANIFEST.sha256.json'
    manifest = load_json(manifest_path)
    for rel in bundle_contract.manifest_scoped_files:
        target = bundle / rel
        if target.exists():
            manifest[rel] = sha256_file(target)
    dump_json(manifest_path, manifest)
    from bcf_primitive.common import digest_data
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


def _make_bundle(tmp_root: Path, profile: Path, name: str) -> Path:
    bundle = tmp_root / name
    if bundle.exists():
        shutil.rmtree(bundle)
    compile_bundle(profile, bundle)
    return bundle


def _apply_mutation(bundle: Path, case: dict[str, Any]) -> None:
    mutation = case['mutation']
    if mutation == 'json_patch':
        _mutate_json_file(bundle / case['target'], case['patch'], case.get('patch_index'))
        if case.get('sync_manifest', True) and case['target'] in bundle_contract.manifest_scoped_files:
            _sync_manifest_and_governance(bundle)
        return
    if mutation == 'claim_tcb_tamper':
        _mutate_json_file(bundle / 'CLAIM.json', {'official_runner_only': False, 'direct_runtime_api_officially_supported': True, 'parallel_families': True})
        _mutate_json_file(bundle / 'TCB_REPORT.json', {'official_runner_only': False})
        _sync_manifest_and_governance(bundle)
        return
    raise ValueError(f'unsupported mutation: {mutation}')


def _run_family(project_root: Path, profile: Path, tmp_root: Path, family_dir: Path) -> dict[str, Any]:
    corpus = _load_json(family_dir / 'cases.json')['cases']
    reports: dict[str, Any] = {}
    overall_ok = True
    for case in corpus:
        bundle = _make_bundle(tmp_root, profile, case['case_id'])
        _apply_mutation(bundle, case)
        primary = verify_bundle(bundle)
        independent = verify_bundle_independent(bundle)
        externalized = verify_bundle_externalized(bundle)
        ok = all([
            primary.get('verification_result') == 'NOT_VERIFIED',
            primary.get('refusal_code') == case['expected_refusal_code'],
            primary.get('refusal_class') == case['expected_refusal_class'],
            independent.get('refusal_code') == case['expected_refusal_code'],
            independent.get('refusal_class') == case['expected_refusal_class'],
            externalized.get('refusal_code') == case['expected_refusal_code'],
            externalized.get('refusal_class') == case['expected_refusal_class'],
            _validate(REFUSAL_SCHEMA, primary)['ok'],
            _validate(REFUSAL_SCHEMA, independent)['ok'],
            _validate(REFUSAL_SCHEMA, externalized)['ok'],
        ])
        overall_ok = overall_ok and ok
        reports[case['case_id']] = {
            'ok': ok,
            'expected': case,
            'primary': _normalize(primary),
            'independent': _normalize(independent),
            'externalized': _normalize(externalized),
        }
    return {'overall_ok': overall_ok, 'cases': reports}


def run_verification_subfamily_completion_harness(project_root: str | Path, profile: str | Path) -> dict[str, Any]:
    project_root = Path(project_root)
    profile = Path(profile)
    tmp_root = project_root / '.verification_subfamily_tmp'
    if tmp_root.exists():
        shutil.rmtree(tmp_root)
    tmp_root.mkdir(parents=True, exist_ok=True)
    base = project_root / 'corpus' / 'adversarial' / 'verification_subfamilies'
    family_reports: dict[str, Any] = {}
    overall_ok = True
    for family_dir in sorted([p for p in base.iterdir() if p.is_dir()]):
        report = _run_family(project_root, profile, tmp_root, family_dir)
        family_reports[family_dir.name] = report
        overall_ok = overall_ok and report['overall_ok']
    shutil.rmtree(tmp_root)
    return {'overall_ok': overall_ok, 'families': family_reports}


if __name__ == '__main__':
    print(json.dumps(run_verification_subfamily_completion_harness(ROOT, ROOT / 'examples' / 'canonical' / 'invoice_profile.json'), indent=2, sort_keys=True))
