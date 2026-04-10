# `SPEC/COMPILED_BACKEND.md`

## 0. Status

This document is the normative compiled-backend specification for **BCF Primitive One**.

Its function is to define, in closed and explicit form, the kernel-scoped compiled execution form that is derived from `ADMISSION_NORMAL_FORM`, preserves admission verdict meaning for the current bounded primitive kernel, and serves as the immediate bridge between reference semantics and future scalable execution backends.

This document is not a claim that the whole primitive family has already been compiled into one final universal intermediate representation.
It is not a solver-completeness claim.
It is not a whole-family backend-correctness proof.

It is the **normative compiled execution form for the current kernel-scoped admission backend line**.

This document must be read together with:

- `SPEC/ADMISSION_NORMAL_FORM.md`
- `SPEC/ADMISSION_NORMAL_FORM_EXECUTABLE_CONTRACT.md`
- `SPEC/ADMISSION_SEMANTICS.md`
- `SPEC/CANONICALIZATION_LAW.md`
- `SPEC/VERIFICATION_LAW.md`
- `SPEC/PRIMITIVE_EQUIVALENCE.md`

---

## 1. Purpose

The current primitive already has:

- reference law
- reference evaluator
- admission normal form

What this layer adds is a **compiled execution representation** that is still exact relative to the current kernel scope, but is more structured for future scalable execution than direct enumerative evaluation alone.

The compiled backend exists to:

1. preserve kernel verdict meaning
2. preserve ANF digest identity
3. provide deterministic indexed execution structure
4. provide a concrete backend artifact in canonical bundles
5. prepare future symbolic / solver-backed execution families
6. remain parity-checkable against reference semantics

---

## 2. Scope boundary

The compiled backend layer is **kernel-scoped**.

It currently covers:

- current ANF atom basis
- current DNF literal-clause representation
- deterministic indexed clause execution
- parity against ANF and reference evaluator on the current kernel corpus
- compiler artifact emission and verifier recomputation

It does **not** yet claim:

- whole-family final IR status
- backend completeness for every future object family
- full solver lowering correctness
- full whole-family mechanized correctness

---

## 3. Canonical statement

The compiled backend of the current line is:

> a deterministic indexed execution form derived from `ADMISSION_NORMAL_FORM`, preserving verdict meaning for the current kernel-scoped admission profile language by compiling stable atom-indexed DNF clause structure into clause-index and literal-index artifacts that can be re-evaluated without changing the primitive law.

---

## 4. Backend form

The current compiled backend form is:

- `source_kind = indexed_dnf_clause_backend_v1`

A valid compiled backend object carries at least:

- `profile_id`
- `source_kind`
- `anf_digest`
- `atom_index`
- `clauses`
- `literal_index`
- `evaluation_order`
- `compilation_trace`
- `backend_digest`

---

## 5. Semantic law

For the current kernel scope, the compiled backend must satisfy:

### 5.1 Deterministic compilation
The same lawful profile must compile to the same backend artifact.

### 5.2 Verdict preservation
For the current kernel corpus, compiled-backend evaluation must yield the same verdict class as:
- the ANF evaluator
- the reference evaluator

### 5.3 Canonical identity preservation
The backend must carry explicit dependency on the ANF digest and must remain schema-valid and verifier-recomputable.

### 5.4 Bundle verifiability
If the compiler emits `COMPILED_BACKEND.json`, the verifier must be able to recompute and compare it.

### 5.5 Non-widening
The compiled backend must not introduce new positive authority beyond the law already carried by the profile and ANF.

---

## 6. Current theorem target

The compiled backend preparation line currently targets these theorem-level obligations:

- deterministic compilation
- backend parity with ANF
- backend parity with reference evaluator
- compiler/verifier backend artifact parity
- schema-valid backend artifact discipline

That is the current compiled backend law.
