# Closure Status Ledger

| Family | Status | Evidence | Blocking gap for next status |
|---|---|---|---|
| `object_model` | `executable_witness` | `SPEC/OBJECT_MODEL.md`, `tests/test_object_canonicalization_impossibility_saturation.py` | full machine-checked closure not claimed |
| `canonicalization` | `executable_witness` | `SPEC/CANONICALIZATION_LAW.md`, `dist/object_canonicalization_impossibility_saturation_report.json` | no theorem-prover final closure |
| `admission` | `executable_witness` | `SPEC/PRIMITIVE_LAW.md`, `tests/test_admission_normal_form.py` | whole-family semantic closure still partial |
| `refusal` | `executable_witness` | `SPEC/REFUSAL_ALGEBRA.md`, `schemas/refusal.schema.json` | formal calculus closure not claimed |
| `permit` | `executable_witness` | `SPEC/PERMIT_ALGEBRA.md`, `schemas/permit.schema.json` | formal calculus closure not claimed |
| `verification` | `independent_parity` | `dist/verification_subfamily_completion_report.json`, `dist/import_independence_report.json` | external independent CI attestation still pending |
| `witness` | `independent_parity` | `dist/witness_certificate_expansion_report.json`, `schemas/witness_certificate.schema.json` | proof-certificate closure not claimed |
| `compiled_backend` | `executable_witness` | `dist/compiled_backend_gate_report.json`, `schemas/compiled_backend.schema.json` | scalable backend completeness not claimed |
| `admission_normal_form` | `executable_witness` | `dist/admission_normal_form_gate_report.json`, `SPEC/ADMISSION_NORMAL_FORM.md` | whole-family IR closure not claimed |
| `mechanized_kernel` | `mechanized_partial` | `PROOFS/MECHANIZED_KERNEL_PREP_REPORT.md`, `mechanized_kernel/semantic_core.py` | whole-family machine-checked discharge absent |
| `python_independence` | `independent_parity` | `dist/import_independence_report.json`, `dist/independent_second_implementation_parity_report.json` | external separate-repo parity execution pending |
| `node_parity` | `independent_parity` | `dist/node_out_of_family_parity_report.json`, `node_second_line/src/index.mjs` | external third-party rerun pending |
