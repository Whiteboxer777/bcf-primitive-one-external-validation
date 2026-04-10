# `SPEC/COMPILED_BACKEND_EXECUTABLE_CONTRACT.md`

## 0. Status

This document fixes the executable-contract discipline for the current compiled-backend preparation family of **BCF Primitive One**.

The controlling surfaces are:

- normative prose: `SPEC/COMPILED_BACKEND.md`
- machine artifact: `COMPILED_BACKEND.json`
- schema: `schemas/compiled_backend.schema.json`
- executable gate: `tools/compiled_backend_gate.py`
- gate report: `dist/compiled_backend_gate_report.json`

This contract is kernel-scoped and does not claim whole-family final IR closure.

---

## 1. Exact contract

The current line requires:

1. compiler emission of `COMPILED_BACKEND.json`
2. compiler emission of `COMPILED_BACKEND.schema.json`
3. verifier recomputation and equality check of compiled backend artifact
4. deterministic recompilation on the current kernel profiles
5. verdict parity against:
   - ANF evaluator
   - reference evaluator
6. report-backed gate execution with `overall_ok = true`

---

## 2. Truth boundary

This executable contract proves:

- compiled-backend preparation exists
- compiled backend is deterministic on the current kernel corpus
- compiled backend is parity-checked against current ANF/reference semantics
- compiled backend is compiler/verifier-artifact checked

It does not prove:

- whole-family backend completeness
- whole-family compiled correctness
- solver backend correctness
- whole-family mechanized discharge

---

## 3. Release discipline

The current compiled-backend preparation family is release-significant and must remain truth-synchronized with:

- adequacy matrix
- theorem discharge ledger
- bundle contract
- compiler emission
- verifier artifact checks

That is the compiled-backend executable contract.
