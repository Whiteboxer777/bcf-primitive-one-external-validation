
# `SPEC/ADMISSION_NORMAL_FORM_EXECUTABLE_CONTRACT.md`

This document defines the executable-contract discipline for Admission Normal Form.

The controlling surfaces are:
- `SPEC/ADMISSION_NORMAL_FORM.md`
- `schemas/admission_normal_form.schema.json`
- `tools/admission_normal_form_gate.py`
- `dist/admission_normal_form_gate_report.json`

The ANF executable contract is satisfied only if:
1. ANF artifacts are emitted by the compiler for fresh bundles
2. verifier surfaces recompute and match the emitted ANF artifact
3. the ANF artifact validates against the ANF schema
4. the ANF evaluator agrees with the reference profile evaluator on the canonical kernel corpus
5. ANF compilation is deterministic and idempotent on the tested kernel corpus

This contract is kernel-scoped and must not be read as whole-family final IR closure.
