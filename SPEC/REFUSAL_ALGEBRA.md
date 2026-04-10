# `SPEC/REFUSAL_ALGEBRA.md`

## 0. Status

This document is the normative refusal-algebra specification for **BCF Primitive One**.
It defines the structure, semantics, classification, completeness, binding, and determinism of refusal as the negative output family of the primitive.

---

## 1. Purpose

The refusal algebra exists to ensure that refusal is:
1. a normative object family, not free-form denial text
2. complete over admission-blocking failure space
3. replayable and audit-stable
4. typed, closed, and non-ambiguous
5. resistant to silent dropping or blurring of defect classes
6. as rigorously structured as the positive half of the primitive

`REFUSAL` is not merely “not-allow”; it is the structured realization of closed-world negative authority.

---

## 2. Core domains

Let:
- `E` be the domain of canonical evaluation contexts
- `F` be the domain of admission-blocking failure conditions
- `RC` be the closed domain of refusal classes
- `RCode` be the closed domain of refusal codes
- `RObj` be the domain of lawful refusal objects

The refusal algebra requires a lawful projection relation:

`ρ : (E × F) -> RObj`

and lawful class/code factorizations:
- `κ_class : (E × F) -> RC`
- `κ_code : (E × F) -> RCode`

---

## 3. Refusal-object form

A lawful refusal object must semantically realize at least:

`Refusal = (primitive_identity, verdict_identity, refusal_class, refusal_code, refusal_binding, replay_binding, refusal_scope)`

Mandatory semantics:
- verdict identity = `REFUSAL`
- primitive identity
- refusal class
- refusal code
- refusal binding to the decision context
- replay binding where required
- refusal scope

Optional human-readable or diagnostic text may accompany refusal, but it is not the algebra.

---

## 4. Closed refusal-class universe

The refusal-class universe must be closed for the active line.
At minimum, the law requires coverage of the following class families:
1. primitive identity / law-line defects
2. canonicalization / identity defects
3. bundle structural defects
4. manifest / content-binding defects
5. verification defects
6. request structural defects
7. request-shape defects
8. request-bounds defects
9. contract-satisfaction defects
10. witness / support-binding defects
11. action-binding defects
12. replay / traceability defects
13. ambiguity / underdetermination defects
14. determinism / equivalence defects

The concrete line may refine these further but may not omit their semantic coverage.

---

## 5. Closed refusal-code universe

Refusal codes must come from a closed law-governed universe.
Every refusal code must:
- have stable semantic meaning
- belong to a lawful refusal class
- be attributable to actual admission-blocking defect patterns
- remain determinable under the active line

Ad hoc denial strings are not lawful substitutes.

---

## 6. Binding and replay

Every lawful refusal must be attributable to the relevant evaluation context through refusal binding.
Refusal binding must connect, where applicable:
- primitive identity
- canonical bundle identity
- canonical request identity
- contract/boundary scope
- defect locus or evaluation stage where relevant

Where replay is required, refusal must also carry replay-stable attribution sufficient to re-establish the same negative decision context in principle.

---

## 7. Completeness law

For every admission-blocking failure condition in a canonical evaluation context, there exists a lawful refusal realization.

There must be no admission-blocking negative remainder that survives only as:
- raw exception
- process abort
- opaque error
- unclassified negative state
- diagnostic-only state without lawful refusal realization

At the normative boundary, such states must land in structured refusal.

---

## 8. Determinism and multi-failure states

For a fixed canonical evaluation context and fixed canonical failure condition, refusal class and refusal code must be lawfully determined.

Multi-failure states may exist. The active line must therefore define deterministic precedence or combination rules sufficient to determine a lawful primary refusal meaning.

A lawful refusal may carry subordinate diagnostics or secondary tags, provided:
- final verdict remains singularly `REFUSAL`
- primary refusal meaning remains explicit
- replay-equivalent primary meaning is preserved

---

## 9. Ambiguity and hidden-state rules

If the system cannot determine which refusal class/code lawfully applies because the defect state itself is materially ambiguous and no lawful disambiguation exists, the algebra must still land in refusal under the ambiguity/underdetermination region of the closed algebra.

Refusal classification must not depend on hidden implementation state not lawfully attributable to the canonical evaluation context.

---

## 10. Relation to canonicalization and admission

Refusal objects that must be replay-stable must themselves be canonically representable under the active law.

The refusal algebra is downstream of final admission `REFUSAL` and defines how that negative verdict is structured. It may not redefine what counts as admission-blocking.

---

## 11. Invariants

Every lawful refusal object satisfies:
- verdict invariant (`REFUSAL`)
- class/code coherence invariant
- binding invariant
- replay invariant where required
- completeness invariant over blockers
- determinism invariant
- non-permissiveness invariant

---

## 12. Theorem commitments

The line commits at minimum to:
- refusal completeness theorem
- no uncoded blocker theorem
- verdict coherence theorem
- class-code coherence theorem
- binding theorem
- replay-attribution theorem
- deterministic classification theorem
- multi-failure primary-refusal theorem
- fail-closed landing theorem
- anti-free-form theorem

---

## 13. Final refusal-algebra law statement

In BCF Primitive One, refusal is the structured negative realization of the final verdict `REFUSAL`, defined over a closed algebra in which every admission-blocking failure condition arising within a canonical evaluation context projects, by law-governed classification and binding rules, to a lawful refusal object carrying the active primitive identity, verdict identity, a closed-world refusal class, a closed-world refusal code, lawful context binding, and replay-stable attribution where required; this algebra is complete over admission-blocking failure space, deterministic for canonical equivalent failure states, closed against ad hoc or free-form negative authority, and fail-closed in the sense that no admission-blocking defect may remain unclassified, permissive, or outside the refusal object universe.

That is the refusal algebra.
