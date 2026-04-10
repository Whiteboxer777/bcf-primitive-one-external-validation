# TRUE_MINIMAL_TRUST_KERNEL_AND_REAL_SECOND_IMPLEMENTATION

## Objective
Compress the primitive to a single authoritative trust-kernel law surface while making the independent Python line materially semantic rather than a thin shell over the shared kernel.

## Concrete changes
- `bcf_trust_kernel` remains the only authoritative shared semantic source for the primary and verifier surfaces.
- `bcf_primitive/admission_normal_form.py` and `bcf_primitive/compiled_backend.py` are reduced to facades over the trust kernel.
- `bcf_primitive_verifier/admission_normal_form.py` and `bcf_primitive_verifier/compiled_backend.py` are reduced to facades over the trust kernel.
- `bcf_primitive/verifier.py` is reduced to a compatibility facade over the official verifier package.
- `bcf_primitive_independent/semantic_core.py` is a standalone second semantic implementation line.
- `bcf_primitive_independent/admission_normal_form.py` and `bcf_primitive_independent/compiled_backend.py` compile from the independent semantic core rather than importing those semantics from `bcf_trust_kernel`.
- `tools/duplicate_surface_gate.py` fails on unauthorized code duplication.
- `tools/artifact_hygiene_gate.py` fails on caches, pyc files, and temporary release debris.

## Claim boundary
This pass materially strengthens implementation independence, but it does not claim theorem-prover closure for the whole family and does not claim OS/hardware non-bypass.
