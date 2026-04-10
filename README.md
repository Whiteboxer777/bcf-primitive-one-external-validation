# BCF Primitive One

BCF Primitive One is a deterministic, fail-closed, verifier-backed admission boundary primitive.

Official positive route:

`source profile -> canonical bundle -> verify bundle -> admission evaluation -> permit -> released action descriptor`

This release is the finalization-oriented primitive line. It contains one ordered normative `SPEC/` law family together with multiple executable realization surfaces:

- primary Python line: `src/bcf_primitive/`
- verifier line: `src/bcf_primitive_verifier/`
- independent Python second implementation: `src/bcf_primitive_independent/`
- externalized Python second line: `externalized_second_line/`
- out-of-family Node.js second line: `node_second_line/`
- theorem-family and adversarial corpora: `corpus/`
- reports and parity evidence: `dist/` and `REPORTS/`
- theorem-discharge evidence ledger: `PROOFS/THEOREM_DISCHARGE_LEDGER.md`

## What it is

A pre-action admission boundary that answers a narrower question than truth, ranking, or planning:

**May this request pass this explicit verified boundary profile, yes or no?**

## What it does

- compiles a source profile into a canonical bundle
- verifies bundle integrity, contract closure, and required boundary artifacts
- evaluates requests under a deterministic fail-closed admission contract
- emits structured refusal objects for negative landing states
- emits structured permit objects for lawful positive passage
- checks parity across multiple implementation lines, including an out-of-family Node.js line
- carries theorem-family corpus, adversarial corpus, and theorem-discharge evidence

## What it is not

- not an open-world truth engine
- not a general policy platform
- not a full compliance system
- not an OS-level or hardware-level non-bypass substrate
- not a substitute for downstream business correctness or downstream execution success
- not a theorem-prover-complete formal proof line

## Normative source

The controlling primitive-law source is the ordered `SPEC/` family.
Start at:

- `SPEC/INDEX.md`

## Release truthfulness boundary

This release contains strong executable-witness evidence, parity evidence, and adversarial closure evidence.
It does **not** claim:

- full theorem-prover discharge
- a fully separate second repository/toolchain with independent CI governance
- hardware-rooted or OS-rooted enforcement

Those remain outside the present release boundary unless separately built.

## Law-to-machine closure artifacts

Primary law-to-machine closure surfaces:

- `SPEC/ADEQUACY_MATRIX.md`
- `LAW_ALIGNMENT_REPORT.md`
- `PROOFS/THEOREM_DISCHARGE_LEDGER.md`
- `dist/equivalence_report.json`
- `dist/theorem_family_corpus_report.json`
- `dist/adversarial_closure_report.json`
- `dist/verification_subfamily_completion_report.json`
- `dist/node_out_of_family_parity_report.json`
- `dist/node_verification_subfamily_parity_report.json`

## Quick start

Create a bundle:

```bash
PYTHONPATH=src python -m bcf_primitive.cli compile examples/canonical/invoice_profile.json --out /tmp/bundle
```

Verify the bundle:

```bash
PYTHONPATH=src python -m bcf_primitive.cli verify-bundle /tmp/bundle
```

Run the sealed boundary:

```bash
PYTHONPATH=src python -m bcf_primitive.cli sealed-run /tmp/bundle examples/canonical/invoice_request_allow.json examples/canonical/action_allow.json
```

Run the Python test suite:

```bash
pytest -q
```

Run the Node.js parity surface:

```bash
python tools/node_out_of_family_parity.py
```

## Externalized second-line repo prep

The release also contains a concrete separate-repo preparation pack for the Node.js out-of-family second implementation line at `repo_exports/node_second_line_repo/`, plus a ready-made export archive at `dist/NODE_SECOND_LINE_REPO_EXPORT.zip`.


Adequacy is controlled by `SPEC/ADEQUACY_MATRIX.md`, mirrored by `SPEC/ADEQUACY_MATRIX.json`, and gated by `SPEC/ADEQUACY_EXECUTABLE_CONTRACT.md` plus `tools/adequacy_matrix_gate.py`.


Additional executable-contract surfaces now present in this release:
- `SPEC/ADEQUACY_EXECUTABLE_CONTRACT.md`
- `SPEC/THEOREM_DISCHARGE_EXECUTABLE_CONTRACT.md`
- `SPEC/CROSS_REPO_PARITY_EXECUTABLE_CONTRACT.md`
- `SPEC/ADEQUACY_MATRIX.json`
- `PROOFS/THEOREM_DISCHARGE_LEDGER.json`
- `SPEC/THEOREM_DISCHARGE_POLICY.json`
- `CI/CROSS_REPO_PARITY_CONTRACT.json`
- `tools/adequacy_matrix_gate.py`
- `tools/theorem_discharge_gate.py`
- `tools/cross_repo_parity_ci_gate.py`


## Truth boundary for cross-repo parity

The current release provides **export-prepared, machine-gated cross-repo parity readiness**. It includes an exported Node repo, workflow templates, local exported-repo reports, and a main-line gate that ingests those reports. It does **not** claim that the Node line is already hosted in a separate external repository or already executed by independent external CI governance.


## Mechanized kernel preparation

This release now also contains a mechanized-kernel preparation surface:
- `mechanized_kernel/semantic_core.py`
- `mechanized_kernel/checker.py`
- `tools/mechanized_kernel_gate.py`
- `PROOFS/MECHANIZED_KERNEL_SCOPE.md`
- `PROOFS/MECHANIZED_THEOREM_MAP.md`
- `PROOFS/PROOF_OBLIGATIONS.md`
- `PROOFS/SEMANTIC_CORE_FORMALIZATION.md`

This surface is intentionally kernel-scoped and does not claim whole-family theorem-prover discharge.

## Final internal RC readiness artifacts

The current line also includes:
- `RC_CLAIM_BOUNDARY.md`
- `RC_RESIDUAL_GAPS.md`
- `FINAL_INTERNAL_RC_READINESS_REPORT.md`
- `tools/final_internal_rc_readiness_gate.py`
- `REPORTS/final_internal_rc_readiness_report.json`



## Admission Normal Form

This RC also includes a kernel-scoped Admission Normal Form line:
- `SPEC/ADMISSION_NORMAL_FORM.md`
- `SPEC/ADMISSION_NORMAL_FORM_EXECUTABLE_CONTRACT.md`
- `schemas/admission_normal_form.schema.json`
- `tools/admission_normal_form_gate.py`
- `dist/admission_normal_form_gate_report.json`

This line fixes a deterministic compiled DNF-literal-clause representation for normalized admission profiles and checks its parity against the reference evaluator on the kernel-scoped corpus.


## Compiled backend preparation

The current release now also contains a kernel-scoped compiled backend line:
- `SPEC/COMPILED_BACKEND.md`
- `SPEC/COMPILED_BACKEND_EXECUTABLE_CONTRACT.md`
- `schemas/compiled_backend.schema.json`
- `tools/compiled_backend_gate.py`
- `dist/compiled_backend_gate_report.json`

This line is preparation-scope only and does not yet claim whole-family compiled-backend correctness.


Witness-certificate line:
- `SPEC/WITNESS_CERTIFICATES.md`
- `SPEC/WITNESS_CERTIFICATES_EXECUTABLE_CONTRACT.md`
- `schemas/witness_certificate.schema.json`
- `tools/witness_certificate_gate.py`
- `dist/witness_certificate_gate_report.json`

## Whole-family mechanization expansion

This release now includes a scoped executable-witness whole-family mechanization expansion line:
- `SPEC/WHOLE_FAMILY_MECHANIZATION_EXPANSION.md`
- `SPEC/WHOLE_FAMILY_MECHANIZATION_EXPANSION_EXECUTABLE_CONTRACT.md`
- `tools/whole_family_mechanization_expansion_gate.py`
- `dist/whole_family_mechanization_expansion_report.json`

Truth boundary: this is an executable-witness expansion over the semantic core, ANF, compiled backend, and witness-certificate lines. It is not a theorem-prover-grade whole-family discharge.


- Object/canonicalization/impossibility saturation line:
  - `SPEC/OBJECT_CANONICALIZATION_IMPOSSIBILITY_SATURATION.md`
  - `SPEC/OBJECT_CANONICALIZATION_IMPOSSIBILITY_SATURATION_EXECUTABLE_CONTRACT.md`
  - `tools/object_canonicalization_impossibility_saturation_gate.py`
  - `dist/object_canonicalization_impossibility_saturation_report.json`


Witness-certificate expansion line:
- SPEC/WITNESS_CERTIFICATE_EXPANSION.md
- SPEC/WITNESS_CERTIFICATE_EXPANSION_EXECUTABLE_CONTRACT.md
- tools/witness_certificate_expansion_gate.py
- dist/witness_certificate_expansion_report.json

## Release surface

The compact canonical release surface is described in:

- `RELEASE_SURFACE.md`
- `RELEASE_STATUS.md`

Historical pass-by-pass narrative reports are retained under:

- `HISTORY/pass_reports/`



## True Minimal Trust Kernel / Real Second Implementation

- shared semantic law now lives authoritatively in `src/bcf_trust_kernel/`
- primary/verifier ANF/backend modules are facades, not duplicated semantic copies
- the independent Python line now owns its own semantic core in `src/bcf_primitive_independent/semantic_core.py`
- duplicate and artifact-hygiene gates are available under `tools/duplicate_surface_gate.py` and `tools/artifact_hygiene_gate.py`
