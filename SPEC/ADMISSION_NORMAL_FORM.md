
# `SPEC/ADMISSION_NORMAL_FORM.md`

## 0. Status

This document is the normative admission-normal-form specification for **BCF Primitive One**.

Its function is to define, in closed and explicit form, the canonical compiled semantic form of a profile-bound admission contract, the exact relation between normalized profile law and clause-level execution form, the semantics of literals and clauses, the determinism and equivalence obligations of the normal-form compiler, and the way later execution backends may lawfully rely on the compiled form without changing primitive meaning.

This document is not an optimization memo.
It is not a generic compiler note.
It is not a suggestion for one possible internal representation.

It is the **normative compiled semantic form** of admission for the kernel-scoped execution line.

---

## 1. Purpose

Admission Normal Form exists to separate:
- reference law meaning
- normalized boolean structure
- compiled execution form

without changing the primitive law.

Its purpose is to provide one deterministic compiled representation that can be:
- generated from the normalized boundary profile
- checked for equality across implementations
- executed by reference or scalable backends
- used as a witness-bearing intermediate artifact
- attached to bundle verification as a compiler product

---

## 2. Scope

Admission Normal Form is kernel-scoped.

It is defined for the profile-root admission fragment handled by the current finite-domain semantic kernel. It is not yet the whole-family final intermediate representation for every future object-model, governance, or deployment extension.

Thus this document claims:
- kernel-scoped admission normal form
- not whole-family universal IR finality

---

## 3. Core definition

For a lawful profile `P`, let `normalize(P.root)` yield the canonical normalized boolean root.

Admission Normal Form (ANF) is the deterministic compiled representation obtained by:
1. normalizing the root
2. converting the normalized root to negation-normal form sufficient for literal compilation
3. collecting the unique atom basis under stable canonical ordering
4. compiling the formula into a disjunction of conjunctions of signed literals
5. eliminating clause-internal contradictions and duplicate clauses
6. serializing the result under canonical ordering

The resulting ANF is a DNF-literal-clause representation.

---

## 4. ANF object structure

A lawful ANF object carries at least:
- `profile_id`
- `source_kind = dnf_literal_clauses`
- `normalized_root`
- `atom_index`
- `clauses`
- `compilation_trace`
- `anf_digest`

### 4.1 Atom index
Each atom entry fixes:
- stable `atom_id`
- atom kind
- optional `rule_id`
- canonical atom object
- atom digest

### 4.2 Clause set
Each clause is a conjunction of signed literals.
The whole ANF is the disjunction of all clauses.

### 4.3 Literal semantics
A literal is:
- positive atom truth, or
- negative atom truth

No literal may refer to an atom outside the atom index.

---

## 5. Semantic law

For every kernel-scoped lawful profile `P` and lawful request `R`:

`Eval(P, R)` and `Eval(ANF(P), R)` must yield the same verdict class.

This is the central equivalence law of Admission Normal Form.

---

## 6. Compiler obligations

A lawful ANF compiler must satisfy:
- deterministic atom ordering
- deterministic clause ordering
- duplicate elimination
- contradiction elimination inside clauses
- stable digest derivation from canonical bytes
- equivalence to normalized profile semantics on the kernel-scoped domain

---

## 7. What ANF is for

ANF exists to support:
- reference semantic checking
- parity between implementations
- future compiled/scalable backends
- future witness/certificate generation
- future stronger mechanization over a fixed intermediate form

ANF is therefore the bridge between:
- law
- normalized profile semantics
- compiled execution

---

## 8. What ANF is not

ANF is not yet:
- a whole-family final IR for every theorem family
- a guarantee of scalability by itself
- a proof that every backend is correct merely because it uses ANF

Those require additional backend-correctness and family-expansion work.

---

## 9. Final law statement

Admission Normal Form in BCF Primitive One is the deterministic kernel-scoped compiled representation of a normalized admission profile into a DNF-literal-clause object with stable atom basis, stable clause basis, stable digest, and verdict-preserving semantics relative to the reference admission evaluator, such that future compiled backends may rely on the same ANF only if they preserve the same admission verdict meaning under the active primitive law.
