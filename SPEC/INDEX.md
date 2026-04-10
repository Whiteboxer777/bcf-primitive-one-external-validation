# `SPEC/INDEX.md`

## 0. Status

This document is the normative specification index for **BCF Primitive One**.

Its function is to define, in closed and explicit form, the ordered structure, authority order, interpretive precedence, document roles, dependency relations, and normative reading discipline of the `SPEC/` law family.

This document is not a convenience table of contents.
It is the **normative entry point and precedence map** for the primitive-law family.

Where ambiguity exists about:
- which specification documents are normative
- how they relate
- which document controls in case of interpretive tension
- what the lawful reading order is
- which documents define meaning versus derive consequences

this document governs.

---

## 1. Canonical normative source

The canonical normative source for **BCF Primitive One** is the `SPEC/` family as ordered and interpreted by this index.

No README, release note, packaging label, build script, CLI help text, audit log, code comment, test name, or historical document may override the `SPEC/` family.

Within the `SPEC/` family, the precedence and dependency rules defined by this index control.

Therefore:

**the source of truth is the ordered `SPEC/` law family inside the canonical main zip.**

---


## 2. Normative documents covered by this index

The following documents are normative members of the current `SPEC/` family:

1. `SPEC/INDEX.md`
2. `SPEC/PRIMITIVE_LAW.md`
3. `SPEC/SCOPE_AND_NON_SCOPE.md`
4. `SPEC/OBJECT_MODEL.md`
5. `SPEC/CANONICALIZATION_LAW.md`
6. `SPEC/VERIFICATION_LAW.md`
7. `SPEC/ADMISSION_SEMANTICS.md`
8. `SPEC/ADMISSION_NORMAL_FORM.md`
9. `SPEC/REFUSAL_ALGEBRA.md`
10. `SPEC/PERMIT_ALGEBRA.md`
11. `SPEC/PRIMITIVE_EQUIVALENCE.md`
12. `SPEC/THEOREM_SET.md`
13. `SPEC/ADEQUACY_MATRIX.md`
14. `SPEC/ADEQUACY_EXECUTABLE_CONTRACT.md`
15. `SPEC/THEOREM_DISCHARGE_EXECUTABLE_CONTRACT.md`
16. `SPEC/CROSS_REPO_PARITY_EXECUTABLE_CONTRACT.md`
17. `SPEC/ADMISSION_NORMAL_FORM_EXECUTABLE_CONTRACT.md`

No other document becomes normative merely by existing in the release.

## 3. Non-normative documents

The following document classes are non-normative unless explicitly incorporated by lawful revision:

- `README.md`
- `CLAIM.md`
- `LIMITS.md`
- `REPRODUCE.md`
- `TCB.md`
- `REFUSAL_CODES.md`
- shell scripts
- Python modules
- tests
- generated manifests
- audit reports
- historical files
- old version markers
- domain examples

These may explain, operationalize, or witness. They do not control primitive meaning.

---

## 4. Canonical role of each normative spec document

### `SPEC/PRIMITIVE_LAW.md`
Defines the primitive identity, verdict universe, official positive path, fail-closed law, closed-world law, and top-level admission law.

### `SPEC/SCOPE_AND_NON_SCOPE.md`
Defines what the primitive does and does not claim. It prevents inflation and erosion.

### `SPEC/OBJECT_MODEL.md`
Defines the closed normative object universe, object roles, and binding-sensitive validity.

### `SPEC/CANONICALIZATION_LAW.md`
Defines canonical form, canonical identity, uniqueness, idempotence, and anti-ambiguity identity law.

### `SPEC/VERIFICATION_LAW.md`
Defines bundle-fitness judgment, `VERIFIED` / `NOT_VERIFIED`, and necessity of verification for lawful `ALLOW`.

### `SPEC/ADMISSION_SEMANTICS.md`
Defines what admission means, including the exact `ALLOW` / `REFUSAL` biconditional.


### `SPEC/ADMISSION_NORMAL_FORM.md`
Defines the deterministic kernel-scoped compiled semantic form of normalized admission profiles as DNF literal clauses.

### `SPEC/REFUSAL_ALGEBRA.md`
Defines structured negative output, refusal classes/codes, and blocker completeness.

### `SPEC/PERMIT_ALGEBRA.md`
Defines structured positive output, permit binding, and bounded positive action authority.

### `SPEC/PRIMITIVE_EQUIVALENCE.md`
Defines when two realizations are the same primitive rather than merely compatible.

### `SPEC/THEOREM_SET.md`
Defines theorem obligations and closure targets of the line.

### `SPEC/ADEQUACY_MATRIX.md`
Defines law-to-machine mapping, executable traceability, corpus witnesses, and adequacy status.

### `SPEC/ADEQUACY_EXECUTABLE_CONTRACT.md`
Defines the machine-readable adequacy contract, executable adequacy gate, and release-blocking adequacy policy.

### `SPEC/INDEX.md`
Defines family ordering, precedence, lawful reading order, and conflict discipline.

---

## 5. Primary, semantic, output, and meta-law layers

### Primary law-definition layer
1. `SPEC/PRIMITIVE_LAW.md`
2. `SPEC/SCOPE_AND_NON_SCOPE.md`
3. `SPEC/OBJECT_MODEL.md`

These control what the primitive is, what it is not, and what normatively exists.

### Semantic law layer
4. `SPEC/CANONICALIZATION_LAW.md`
5. `SPEC/VERIFICATION_LAW.md`
6. `SPEC/ADMISSION_SEMANTICS.md`

These control identity, boundary fitness, and final admission meaning.

### Output law layer
7. `SPEC/REFUSAL_ALGEBRA.md`
8. `SPEC/PERMIT_ALGEBRA.md`

These control lawful negative and positive output realization.

### Meta-law layer
9. `SPEC/PRIMITIVE_EQUIVALENCE.md`
10. `SPEC/THEOREM_SET.md`
11. `SPEC/WITNESS_CERTIFICATES.md`
12. `SPEC/WITNESS_CERTIFICATES_EXECUTABLE_CONTRACT.md`
11. `SPEC/ADEQUACY_MATRIX.md`
12. `SPEC/INDEX.md`

These control sameness, theorem closure, law-to-machine mapping, and interpretive discipline.

---

## 6. Canonical reading order

The lawful reading order is fixed as follows:

1. `SPEC/INDEX.md`
2. `SPEC/PRIMITIVE_LAW.md`
3. `SPEC/SCOPE_AND_NON_SCOPE.md`
4. `SPEC/OBJECT_MODEL.md`
5. `SPEC/CANONICALIZATION_LAW.md`
6. `SPEC/VERIFICATION_LAW.md`
7. `SPEC/ADMISSION_SEMANTICS.md`
8. `SPEC/REFUSAL_ALGEBRA.md`
9. `SPEC/PERMIT_ALGEBRA.md`
10. `SPEC/PRIMITIVE_EQUIVALENCE.md`
11. `SPEC/THEOREM_SET.md`
12. `SPEC/ADEQUACY_MATRIX.md`
13. `SPEC/ADEQUACY_EXECUTABLE_CONTRACT.md`
13. `SPEC/ADEQUACY_EXECUTABLE_CONTRACT.md`
12. `SPEC/ADEQUACY_MATRIX.md`
13. `SPEC/ADEQUACY_EXECUTABLE_CONTRACT.md`

This order is canonical because the dependency structure is not flat.

---

## 7. Dependency graph

- `PRIMITIVE_LAW` is the primary law anchor.
- `SCOPE_AND_NON_SCOPE` depends on `PRIMITIVE_LAW` and constrains interpretation of all later documents.
- `OBJECT_MODEL` depends on `PRIMITIVE_LAW` and `SCOPE_AND_NON_SCOPE`.
- `CANONICALIZATION_LAW` depends on `PRIMITIVE_LAW`, `SCOPE_AND_NON_SCOPE`, and `OBJECT_MODEL`.
- `VERIFICATION_LAW` depends on `PRIMITIVE_LAW`, `SCOPE_AND_NON_SCOPE`, `OBJECT_MODEL`, and `CANONICALIZATION_LAW`.
- `ADMISSION_SEMANTICS` depends on `PRIMITIVE_LAW`, `SCOPE_AND_NON_SCOPE`, `OBJECT_MODEL`, `CANONICALIZATION_LAW`, and `VERIFICATION_LAW`.
- `REFUSAL_ALGEBRA` depends on `PRIMITIVE_LAW`, `SCOPE_AND_NON_SCOPE`, `OBJECT_MODEL`, `CANONICALIZATION_LAW`, and `ADMISSION_SEMANTICS`.
- `PERMIT_ALGEBRA` depends on `PRIMITIVE_LAW`, `SCOPE_AND_NON_SCOPE`, `OBJECT_MODEL`, `CANONICALIZATION_LAW`, `VERIFICATION_LAW`, and `ADMISSION_SEMANTICS`.
- `PRIMITIVE_EQUIVALENCE` depends on all primary, semantic, and output laws.
- `THEOREM_SET` depends on the full law family.
- `ADEQUACY_MATRIX` depends on the full law family because it maps law to machine.

---

## 8. Precedence order in case of interpretive tension

### Highest-precedence interpretation rules
1. `SPEC/INDEX.md` controls family ordering, dependency, and conflict discipline.
2. `SPEC/PRIMITIVE_LAW.md` controls what the primitive is.
3. `SPEC/SCOPE_AND_NON_SCOPE.md` controls lawful interpretation boundaries.

### Structural precedence
Where tension concerns what objects exist or how identity is fixed:
- `SPEC/OBJECT_MODEL.md`
- `SPEC/CANONICALIZATION_LAW.md`
control.

### Verification versus admission
- `SPEC/VERIFICATION_LAW.md` controls bundle fitness.
- `SPEC/ADMISSION_SEMANTICS.md` controls request passage under a verified boundary.

### Output precedence
- `SPEC/REFUSAL_ALGEBRA.md` controls structured negative output.
- `SPEC/PERMIT_ALGEBRA.md` controls structured positive output.

### Meta-law boundedness
- `SPEC/PRIMITIVE_EQUIVALENCE.md`, `SPEC/THEOREM_SET.md`, and `SPEC/ADEQUACY_MATRIX.md`
are normative but do not override primary law-definition or semantic law.

---

## 9. Conflict-resolution law

If apparent conflict arises:

1. determine whether the documents operate at different law levels
2. apply the dependency graph
3. apply the precedence order
4. apply scope constraints
5. choose the interpretation that preserves:
   - closed-world discipline
   - fail-closed behavior
   - no-bypass behavior
   - deterministic replay
   - structured permit/refusal meaning

If true contradiction remains:
- higher-precedence document controls
- lower-precedence statement is non-controlling to the extent of contradiction
- the main line has revision debt and must be fixed explicitly

A true contradiction must not be silently tolerated.

---

## 10. Law-over-code rule

The `SPEC/` family defines the primitive normatively.
Code realizes the primitive only if it conforms to the `SPEC/` family.

Therefore:
- code cannot redefine law
- tests cannot redefine law
- build artifacts cannot redefine law
- release notes cannot redefine law

The correct direction is:
**`SPEC/` -> implementation -> tests/audit/equivalence**

---

## 11. Main-zip integration rule

The `SPEC/` family must exist inside the canonical main zip as the official normative law source.

There must not be multiple competing primitive-law sources inside the main zip.
Therefore:
- overlapping old law sheets
- stale version-law docs
- duplicate primitive-definition files
- conflicting quasi-normative summaries

must be removed, archived as non-normative, or explicitly subordinated.

Non-spec documents inside the zip must reference the `SPEC/` family as the controlling law source.

---

## 12. Theorem commitments of the index

### T-INDEX-1 — Single normative family theorem
The normative source of primitive meaning is the ordered `SPEC/` family, not an unordered release corpus.

### T-INDEX-2 — Precedence theorem
If two spec statements appear to conflict, the higher-precedence document under this index controls.

### T-INDEX-3 — Dependency theorem
Downstream-derived documents may not override upstream-defining documents.

### T-INDEX-4 — Scope-preservation theorem
All spec documents must be interpreted under `SPEC/SCOPE_AND_NON_SCOPE.md`.

### T-INDEX-5 — Law-over-code theorem
Implementation, tests, packaging, and release artifacts are subordinate to the `SPEC/` family for primitive meaning.

### T-INDEX-6 — No-duplicate-source theorem
There must not be multiple competing normative primitive-law sources inside the main zip.

### T-INDEX-7 — Canonical reading-order theorem
The lawful interpretive reading order of the spec family is fixed by this document.

### T-INDEX-8 — Meta-law boundedness theorem
`PRIMITIVE_EQUIVALENCE`, `THEOREM_SET`, and `ADEQUACY_MATRIX` govern sameness, closure, and law-to-machine traceability but do not override primary primitive law-definition.

---

## 13. Final index law statement

The `SPEC/` family of BCF Primitive One is a single ordered normative law stack whose controlling source is the set of spec documents enumerated in this index, interpreted under the canonical reading order, dependency graph, and precedence rules fixed here, such that `PRIMITIVE_LAW` and `SCOPE_AND_NON_SCOPE` anchor primitive meaning and lawful interpretation, `OBJECT_MODEL`, `CANONICALIZATION_LAW`, `VERIFICATION_LAW`, and `ADMISSION_SEMANTICS` define the structural and semantic core, `REFUSAL_ALGEBRA` and `PERMIT_ALGEBRA` define lawful output realizations, `PRIMITIVE_EQUIVALENCE` and `THEOREM_SET` define sameness and closure obligations, and `ADEQUACY_MATRIX` defines law-to-machine traceability, with the further law that no non-spec document, code artifact, packaging artifact, historical file, or informal summary may override this ordered family as the normative source of primitive meaning.

That is the specification index.

### `SPEC/ADMISSION_NORMAL_FORM_EXECUTABLE_CONTRACT.md`
Defines the executable-contract surfaces, schema, gate, and audit report for Admission Normal Form.


## Compiled-backend family role

`SPEC/COMPILED_BACKEND.md` defines the kernel-scoped compiled execution form derived from ANF.

`SPEC/COMPILED_BACKEND_EXECUTABLE_CONTRACT.md` defines the executable contract, gate, and report discipline for that compiled-backend preparation family.


## Witness certificate role

`SPEC/WITNESS_CERTIFICATES.md` defines the kernel-scoped evidence-carrying witness-certificate family. `SPEC/WITNESS_CERTIFICATES_EXECUTABLE_CONTRACT.md` defines its executable contract, schema, gate, and audit artifacts.


## Additional normative expansion members

The current law family also includes the following executable-witness expansion documents:
- `SPEC/WHOLE_FAMILY_MECHANIZATION_EXPANSION.md`
- `SPEC/WHOLE_FAMILY_MECHANIZATION_EXPANSION_EXECUTABLE_CONTRACT.md`

These documents are subordinate to the primary law-definition, semantic law, output law, and meta-law documents. They define the scoped mechanization-expansion bridge across the existing semantic core, ANF, compiled backend, and witness-certificate lines.
