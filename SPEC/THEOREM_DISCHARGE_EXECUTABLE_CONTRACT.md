# `SPEC/THEOREM_DISCHARGE_EXECUTABLE_CONTRACT.md`

## 0. Status

This document is the executable-contract specification for theorem discharge in **BCF Primitive One**.

Its function is to bind the theorem-discharge ledger to machine-readable mirrors, a closed status vocabulary, an executable gate, required report artifacts, and release-blocking families, so that theorem discharge is not merely described but mechanically checked.

This document is normative for theorem-discharge contract discipline. It does **not** claim theorem-prover discharge. It governs only executable-witness theorem discharge within the current primitive line.

The theorem-discharge executable-contract surface consists exactly of:

- `PROOFS/THEOREM_DISCHARGE_LEDGER.md`
- `PROOFS/THEOREM_DISCHARGE_LEDGER.json`
- `SPEC/THEOREM_DISCHARGE_POLICY.json`
- `tools/theorem_discharge_gate.py`
- `REPORTS/theorem_discharge_gate_report.json`
- `dist/theorem_discharge_gate_report.json`

## 1. Canonical rule

The markdown ledger is the human-readable normative ledger.
The JSON ledger is the machine-readable mirror.
The policy file fixes the closed status vocabulary, release-blocking theorem families, allowed partial theorem families, and required supporting reports.
The gate is the executable checker.
The gate reports are the inspectable audit artifacts.

## 2. Closed status vocabulary

Only the following theorem-discharge statuses are lawful in the executable contract:

- `EXECUTABLE_WITNESS_STRONG`
- `EXECUTABLE_WITNESS_PARTIAL`
- `LAW_ONLY`
- `MISSING`
- `OUT_OF_SCOPE`

## 3. Release-blocking theorem families

The current release-blocking theorem families are:

- `primitive_identity`
- `verification`
- `admission`
- `refusal`
- `permit`
- `determinism_replay`
- `fail_closed`
- `no_bypass`
- `equivalence`

These theorem families must not fall below `EXECUTABLE_WITNESS_STRONG` in a releasable line.

## 4. Gate obligations

The executable gate must at minimum check:

- existence of the markdown ledger
- existence of the JSON mirror
- exact family-key parity between them
- closed status-vocabulary conformance
- that every release-blocking family is `EXECUTABLE_WITNESS_STRONG`
- that only policy-allowed families remain `EXECUTABLE_WITNESS_PARTIAL`
- that all required report artifacts exist and, where they expose `overall_ok`, that it is `true`
- that each theorem family exposes concrete witness/report references in the JSON mirror

## 5. Output artifact

The executable gate must emit:

- `REPORTS/theorem_discharge_gate_report.json`
- `dist/theorem_discharge_gate_report.json`

These reports are the official machine-audit surface for theorem-discharge contract conformance.


## Exact status discipline

The theorem-discharge contract is not status-permissive. Theorem-family statuses are exact release-line truth claims, not optimistic summaries.

For the current line, the exact expected theorem-family statuses are fixed by `SPEC/THEOREM_DISCHARGE_POLICY.json`. The executable gate must reject stale-strong drift, stale-partial drift, and missing-family drift.

In particular, the following families are intentionally `EXECUTABLE_WITNESS_PARTIAL` in the current line and must not be silently upgraded without new evidence:
- scope
- object_model
- canonicalization
- impossibility
- closure

The remaining core verdict-bearing boundary families are required to remain `EXECUTABLE_WITNESS_STRONG`.


## Mechanized-kernel preparation coupling

The theorem-discharge executable contract now also includes a mechanized-kernel preparation family.
This family is deliberately narrower than whole-family theorem discharge. It is allowed to be marked `EXECUTABLE_WITNESS_STRONG` only because its scope is explicitly restricted to the finite-state semantic kernel and canonicalization subset defined in the proof documents and gate reports.
It must not be read as whole-family theorem-prover discharge.


## Admission normal form preparation family

The theorem-discharge line now includes an `admission_normal_form_preparation` family. This family is release-blocking at `EXECUTABLE_WITNESS_STRONG` within its kernel-scoped meaning only. It is satisfied by the ANF compiler artifact, ANF verifier recomputation, and the ANF gate report. It does not claim whole-family final IR closure.


## Compiled backend preparation coupling

The current theorem-discharge contract also includes the compiled-backend preparation family.

This family is `EXECUTABLE_WITNESS_STRONG` only if:

- `dist/compiled_backend_gate_report.json` is green
- compiler emits compiled backend artifacts
- verifier recomputes and checks those artifacts
- compiled backend preserves verdict class on the current kernel corpus relative to ANF and reference evaluation

This does not claim whole-family compiled-backend correctness.

## Witness certificate preparation coupling

The current line also treats the witness-certificate preparation family as release-blocking strong executable witness discipline. This is bounded to schema-closed, digest-bound verification/permit/refusal witness certificates and does not claim whole-family proof certificates.


## Whole-family mechanization expansion coupling

The theorem-discharge contract now includes a scoped executable-witness whole-family mechanization expansion family.

Its truth boundary is narrow: it witnesses cross-layer coherence among the mechanized kernel, ANF, compiled backend, and witness-certificate lines on the canonical kernel corpus and selected fail-closed / no-bypass boundary paths. It does not claim theorem-prover-grade whole-family discharge.

## Additional strengthened families

The current line now includes a dedicated executable saturation family:

- `object_canonicalization_impossibility_saturation`

This family is allowed to be marked `EXECUTABLE_WITNESS_STRONG` because it is backed by a dedicated saturation gate, dedicated corpus artifacts, and dedicated report artifacts for object-model, canonicalization, and impossibility law regions.


## Witness certificate expansion family

`witness_certificate_expansion` is a scoped executable-witness family that strengthens the evidence-carrying line across runtime, replay, verification, and sample-bundle witness artifacts. It is expected to remain `EXECUTABLE_WITNESS_STRONG` while still not claiming theorem-prover-grade certificate proof discharge.
