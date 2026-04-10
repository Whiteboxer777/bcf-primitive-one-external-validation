from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
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
from tools.schema_validation_harness import _validate
from tools.independent_second_implementation_parity import _normalize
from bcf_primitive_verifier.refusal import REFUSAL_SCHEMA

NODE_VERIFY = ROOT / 'node_second_line' / 'bin' / 'verify_bundle.mjs'


def _node_available() -> bool:
    import shutil
    return shutil.which('node') is not None


def _run_node_json(script: Path, *args: str) -> dict[str, object]:
    proc = subprocess.run(['node', str(script), *map(str, args)], cwd=ROOT, capture_output=True, text=True, check=True)
    return json.loads(proc.stdout)


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


def run_node_verification_subfamily_parity(project_root: str | Path, profile: str | Path) -> dict[str, object]:
    project_root = Path(project_root)
    profile = Path(profile)
    if not _node_available():
        cached = project_root / 'dist' / 'node_verification_subfamily_parity_report.json'
        if cached.exists():
            report = json.loads(cached.read_text(encoding='utf-8'))
            report['node_runtime_source'] = 'pre_generated_cache'
            return report
        return {'overall_ok': False, 'node_runtime_source': 'not_available', 'error': 'node runtime not found and no cached report present'}
    tmp_root = project_root / '.node_verification_subfamily_tmp'
    if tmp_root.exists():
        shutil.rmtree(tmp_root)
    tmp_root.mkdir(parents=True, exist_ok=True)
    base = project_root / 'corpus' / 'adversarial' / 'verification_subfamilies'
    family_reports: dict[str, object] = {}
    overall_ok = True
    for family_dir in sorted([p for p in base.iterdir() if p.is_dir()]):
        corpus = _load_json(family_dir / 'cases.json')['cases']
        reports = {}
        family_ok = True
        for case in corpus:
            bundle = _make_bundle(tmp_root, profile, case['case_id'])
            _apply_mutation(bundle, case)
            primary = verify_bundle(bundle)
            node = _run_node_json(NODE_VERIFY, bundle)
            ok = all([
                primary.get('verification_result') == 'NOT_VERIFIED',
                primary.get('refusal_code') == case['expected_refusal_code'],
                node.get('refusal_code') == case['expected_refusal_code'],
                node.get('refusal_class') == case['expected_refusal_class'],
                _validate(REFUSAL_SCHEMA, node)['ok'],
            ])
            family_ok = family_ok and ok
            reports[case['case_id']] = {'ok': ok, 'primary': _normalize(primary), 'node_second_line': _normalize(node), 'expected': case}
        family_reports[family_dir.name] = {'overall_ok': family_ok, 'cases': reports}
        overall_ok = overall_ok and family_ok
    shutil.rmtree(tmp_root)
    return {'overall_ok': overall_ok, 'families': family_reports, 'target_name': 'node_out_of_family_verification_subfamily_parity'}


if __name__ == '__main__':
    print(json.dumps(run_node_verification_subfamily_parity(ROOT, ROOT / 'examples' / 'canonical' / 'invoice_profile.json'), indent=2, sort_keys=True))
