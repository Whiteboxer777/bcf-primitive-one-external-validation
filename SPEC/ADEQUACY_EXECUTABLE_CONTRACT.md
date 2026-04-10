# `SPEC/ADEQUACY_EXECUTABLE_CONTRACT.md`

## 0. Status

This document is the normative executable-contract companion to `SPEC/ADEQUACY_MATRIX.md` for **BCF Primitive One**.

Its function is to define, in closed and explicit form, how the adequacy matrix becomes machine-checkable, release-governing, and parity-gating rather than remaining only a human-readable ledger.

This document is not a duplicate of the adequacy matrix.
It is not a loose CI note.
It is not a convenience script description.

It is the **executable adequacy contract** of the current primitive line.

This document must be read together with:

- `SPEC/ADEQUACY_MATRIX.md`
- `SPEC/ADEQUACY_MATRIX.json`
- `SPEC/INDEX.md`
- `SPEC/THEOREM_SET.md`
- `SPEC/PRIMITIVE_EQUIVALENCE.md`

---

# 1. Canonical contract statement

The adequacy matrix is authoritative in human-readable form, but it must also be mirrored into a machine-readable contract and checked by an executable gate.

Therefore the current line fixes the following contract:

1. `SPEC/ADEQUACY_MATRIX.md` remains the normative prose ledger
2. `SPEC/ADEQUACY_MATRIX.json` is the machine-readable contract mirror of that ledger
3. `tools/adequacy_matrix_gate.py` is the executable gate for matrix integrity, witness presence, and release-blocking adequacy policy
4. `SPEC/ADEQUACY_RELEASE_POLICY.json` is the machine-readable release-blocking policy consumed by the gate
5. `dist/adequacy_matrix_gate_report.json` is the inspectable audit artifact emitted by the gate

No release line claiming this pass may omit any of these five artifacts.

---

# 2. Closed contract obligations

The executable adequacy contract fixes the following obligations.

## 2.1 Mirror obligation
`SPEC/ADEQUACY_MATRIX.json` must represent the same law rows and gap rows as the markdown matrix.

## 2.2 Status-vocabulary obligation
Only the closed status set may appear:
- `FULL`
- `PARTIAL`
- `LAW_ONLY`
- `MISSING`
- `OUT_OF_SCOPE`

## 2.3 Traceability obligation
Every law row must carry exact values for:
- `LAW_UNIT_ID`
- `LAW_SOURCE`
- `LAW_CLAIM`
- `EXEC_SURFACE`
- `CORPUS_SURFACE`
- `EXPECTED_OBSERVABLE`
- `AUDIT_EVIDENCE`
- `ADEQUACY_STATUS`
- `GAP_NOTES`

## 2.4 Release-blocking obligation
Rows designated by `SPEC/ADEQUACY_RELEASE_POLICY.json` as release-blocking must be `FULL`.

## 2.5 Audit-artifact obligation
Every report path named in the release policy must exist and, where the artifact exposes an `overall_ok` field, it must be `true`.

## 2.6 No-missing-core obligation
No release-blocking law region may contain `MISSING` or `LAW_ONLY` rows.

---

# 3. Release-blocking classes

The current line treats the following law regions as release-blocking for the canonical main zip:

- spec-family anchoring (`IDX-*`)
- primitive-law core (`PL-*`)
- admission core (`AS-*`)
- refusal algebra core (`RA-*`)
- permit algebra core (`PA-*`)
- no-bypass core (`NB-*`)
- theorem-family saturation (`THF-*`)
- theorem-family witness coverage (`THM-*`)
- externalized second-line contract rows (`EXT-*`)
- theorem-discharge row (`TD-*`)

The following rows are currently allowed to remain `PARTIAL` without blocking release because the law line itself declares them as residual closure gaps rather than release-fatal defects:

- `C14N-06`
- `EQ-07`

Verification-subfamily rows `VF-07`, `VF-08`, `VF-09`, `VF-10`, `VF-12`, `VF-13`, and `VF-14` have been truth-synchronized to `FULL` because dedicated adversarial verification-subfamily corpus families and parity reports are now present in the current line.

No other `PARTIAL` row is allowed by the current release policy.

---

# 4. Gate semantics

The adequacy matrix gate must check, at minimum:

1. markdown matrix exists
2. json matrix exists
3. row counts match
4. all statuses are inside the closed vocabulary
5. no duplicate `LAW_UNIT_ID` exists
6. release-blocking rows are `FULL`
7. allowed partial rows are exactly the ones declared by policy
8. every required report artifact exists
9. every required report artifact with `overall_ok` exposes `true`
10. every release-blocking row references at least one concrete audit artifact path that exists in the release tree

---

# 5. Final executable-contract statement

The adequacy matrix of BCF Primitive One is not merely descriptive in the current line; it is mirrored into machine-readable contract form, governed by an explicit release-blocking policy, and enforced by an executable adequacy gate such that row integrity, status legality, report presence, and release-critical adequacy completion are directly checkable inside the canonical zip.
