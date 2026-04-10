# `SPEC/PRIMITIVE_EQUIVALENCE.md`

## 0. Status

This document is the normative primitive-equivalence specification for **BCF Primitive One**.
It defines when an implementation, verifier, runner, library, packaged release, replay engine, or other executable realization may lawfully count as **the same primitive** rather than a merely similar or compatible system.

---

## 1. Purpose

Primitive equivalence exists to prevent:
1. name-preserving semantic drift
2. surface conformance without semantic conformance
3. convenience weakening of fail-closed or no-bypass behavior
4. identity drift
5. false portability claims

Equivalence asks:
> for the same canonical law-governed context, do two realizations preserve the same primitive identity, verdict universe, admission meaning, verification meaning, canonical identity law, permit/refusal meaning, and no-bypass/fail-closed behavior?

---

## 2. Equivalence relation

Let `Impl` denote the domain of candidate primitive realizations.

Primitive equivalence is the law-relative relation:

`≡_Prim`

over `Impl`, such that for realizations `I1` and `I2`:

`I1 ≡_Prim I2`

means that under the active law line, `I1` and `I2` realize the same primitive at the normative boundary.

Equivalence is stronger than compatibility and weaker than source-code identity.

---

## 3. Dimensions that must be preserved

Full primitive equivalence requires preservation of all of the following:
1. primitive identity
2. final verdict universe
3. lawful scope and non-scope
4. object-family meaning
5. admission semantics
6. verification semantics
7. canonicalization and identity law
8. refusal algebra
9. permit algebra
10. official positive-path discipline
11. fail-closed behavior
12. closed-world behavior
13. replay-attributable meaning where required
14. absence of hidden extra positive authority
15. absence of hidden weakening of blockers

---

## 4. Primitive identity preservation

Equivalent realizations must preserve:
- canonical primitive name meaning
- primitive class meaning
- verdict-universe meaning
- law-line reference
- object-model compatibility meaning

Any silent redefinition of these breaks equivalence.

---

## 5. Verdict-universe preservation

Equivalent realizations must preserve the final verdict universe:
`{ALLOW, REFUSAL}`

Where verification is separately realized, they must also preserve the verification-law meaning of:
- `VERIFIED`
- `NOT_VERIFIED`

No third final verdict may appear in one realization if absent in the other.

---

## 6. Admission, verification, and canonicalization preservation

Equivalent realizations must preserve:
- the admission biconditional
- verification necessity for lawful `ALLOW`
- the same canonicalization law for all identity-relevant normative objects

Non-equivalence arises if one realization:
- allows without verification
- weakens blocker handling
- canonicalizes identity-bearing objects differently in an admission-relevant way
- guesses through ambiguity
- preserves no-bypass less strictly

---

## 7. Output preservation

Equivalent realizations must preserve:
- refusal as structured negative output with lawful class/code/binding meaning
- permit as structured positive output with lawful binding and bounded action authority
- replay-equivalent output meaning where required

Implementations need not share source code, but must converge to the same lawful refusal and permit meanings at the normative boundary.

---

## 8. Closed-world, fail-closed, and no-bypass preservation

Equivalent realizations must preserve:
- closed-world admissibility
- fail-closed landing for admission-relevant blockers
- the official positive path in normative effect
- no lawful positive authority outside that path

A hidden or undocumented positive override path is non-equivalent to the primitive line.

---

## 9. Replay-equivalence preservation

For replay-equivalent canonical contexts under the same law line, equivalent realizations must preserve:
- same final verdict
- compatible verification result
- compatible refusal meaning where negative
- compatible permit meaning where positive
- compatible identity bindings where replay requires them

No hidden local information may be required to preserve boundary meaning.

---

## 10. Internal diversity allowed

Equivalent realizations may differ in:
- source code
- programming language
- packaging
- internal data structures
- performance characteristics
- internal optimization strategy
- diagnostic richness

These differences are allowed only if they do not leak into law-governed boundary meaning.

---

## 11. Wrappers and partial realizations

A domain-specific wrapper remains primitive-equivalent only if it does not alter primitive-law semantics.
A verifier-only or replay-only artifact may be subsystem-equivalent without being a full primitive-equivalent realization of the entire primitive.

---

## 12. Equivalence relation properties

Under a fixed law line:
- reflexive
- symmetric
- transitive

Cross-line comparison without explicit revision mapping is outside this relation.

---

## 13. Evidence surface

Primitive equivalence must be witnessed by:
- law-sheet conformance
- canonical corpus agreement on lawful cases
- fail-closed corpus agreement on blocker cases
- verification parity on canonical bundles
- permit/refusal parity in normative meaning
- replay parity where required

The corpus witnesses equivalence; the law defines equivalence.

---

## 14. Drift categories that break equivalence

Any one of the following breaks full equivalence:
- primitive drift
- verdict drift
- admission drift
- verification drift
- canonicalization drift
- refusal drift
- permit drift
- scope drift
- fail-closed drift
- no-bypass drift

---

## 15. Theorem commitments

The line commits at minimum to:
- primitive-identity theorem
- verdict-equivalence theorem
- admission-equivalence theorem
- verification-equivalence theorem
- canonicalization-equivalence theorem
- refusal-equivalence theorem
- permit-equivalence theorem
- fail-closed-equivalence theorem
- no-bypass-equivalence theorem
- replay-equivalence theorem

---

## 16. Final primitive-equivalence law statement

Two realizations are the same primitive, in the sense of BCF Primitive One, if and only if under the same active primitive law line they preserve the same primitive identity, the same lawful scope, the same verdict universe, the same object-model meanings, the same admission and verification semantics, the same canonicalization and identity law, the same structured refusal and permit meanings, the same closed-world fail-closed and no-bypass boundary behavior, and the same replay-attributable normative meaning for canonical equivalent contexts, such that no hidden authority, semantic widening, semantic erosion, or law-governed drift exists between them at the primitive boundary; otherwise they are not equivalent realizations of the same primitive, even if they share formats, names, code ancestry, or partial compatibility.

That is primitive equivalence.
