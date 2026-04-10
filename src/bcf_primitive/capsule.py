from __future__ import annotations
import shutil
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

def _copytree(src: Path, dst: Path) -> None:
    if dst.exists(): shutil.rmtree(dst)
    shutil.copytree(src, dst)

def build_standalone_verifier_release(project_root: str | Path, out_zip: str | Path) -> dict[str, object]:
    project_root = Path(project_root); out_zip = Path(out_zip); stage = out_zip.parent / 'standalone_verifier_release_root'
    if stage.exists(): shutil.rmtree(stage)
    stage.mkdir(parents=True); (stage / 'src').mkdir()
    _copytree(project_root / 'src' / 'bcf_primitive_verifier', stage / 'src' / 'bcf_primitive_verifier')
    _copytree(project_root / 'src' / 'bcf_primitive_independent', stage / 'src' / 'bcf_primitive_independent')
    _copytree(project_root / 'node_second_line', stage / 'node_second_line')
    _copytree(project_root / 'schemas', stage / 'schemas')
    _copytree(project_root / 'SPEC', stage / 'SPEC')
    _copytree(project_root / 'PROOFS', stage / 'PROOFS')
    for rel in [
        'tools/verify_bundle.py','tools/replay_verdict.py','tools/audit_bundle.py','tools/equivalence_harness.py',
        'tools/schema_validation_harness.py','tools/second_surface_parity_target.py','tools/independent_second_implementation_parity.py',
        'tools/theorem_family_corpus_harness.py','tools/adversarial_closure_harness.py','tools/verification_subfamily_completion_harness.py',
        'tools/externalized_second_line_parity.py','tools/node_out_of_family_parity.py','tools/node_verification_subfamily_parity.py',
        'tools/theorem_discharge_ledger.py','tools/compiled_backend_gate.py','tools/witness_certificate_gate.py',
        'tools/admission_normal_form_gate.py','tools/mechanized_kernel_gate.py','tools/whole_family_mechanization_expansion_gate.py',
        'tools/object_canonicalization_impossibility_saturation_gate.py','tools/witness_certificate_expansion_gate.py',
        'VERIFIER_TCB.md','CLAIM.md','LIMITS.md','REPRODUCE.md',
        'corpus/canonicalization/README.md','corpus/canonicalization/request_semantically_equal_a.json',
        'corpus/canonicalization/request_semantically_equal_b.json','corpus/canonicalization/request_distinct.json',
        'corpus/equivalence/README.md','corpus/equivalence/allow_request.json','corpus/equivalence/deny_request.json'
    ]:
        src = project_root / rel; dst = stage / rel; dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, dst)
    _copytree(project_root / 'corpus' / 'theorem_families', stage / 'corpus' / 'theorem_families')
    _copytree(project_root / 'corpus' / 'adversarial', stage / 'corpus' / 'adversarial')
    if out_zip.exists(): out_zip.unlink()
    with ZipFile(out_zip, 'w', compression=ZIP_DEFLATED) as zf:
        for p in sorted(stage.rglob('*')):
            if p.is_file(): zf.write(p, p.relative_to(stage))
    return {'overall_ok': out_zip.exists(), 'zip_path': str(out_zip), 'file_count': sum(1 for p in stage.rglob('*') if p.is_file())}
