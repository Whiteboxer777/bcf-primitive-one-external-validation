# `SPEC/THEOREM_SET.md`

## 0. Status

This document is the normative theorem-set specification for **BCF Primitive One**.
It states the theorem obligations, invariants, preservation claims, impossibility claims, and derived consequences that collectively define the formal closure target of the primitive line.

It is the **normative theorem ledger** of the primitive line.

---

## 1. Purpose

The theorem set provides:
1. the proposition inventory that later proofs, mechanizations, corpora, and audits must target
2. the closure skeleton of the primitive line
3. the bridge between prose-law and mechanized-law
4. the exact statement of what must remain invariant across equivalent realizations

---

## 2. Global semantic setting

Let:
- `P` range over primitive-law-compatible primitive identities
- `B` range over candidate admission bundles
- `R` range over candidate requests
- `E` range over canonical evaluation contexts
- `A` range over canonical admitted contexts
- `F` range over admission-blocking failure conditions
- `U = B*` be the finite byte-string universe
- `V = {ALLOW, REFUSAL}` be the final verdict universe
- `VV = {VERIFIED, NOT_VERIFIED}` be the verification-result universe

All theorems below are scoped by the lawful boundary of BCF Primitive One.

---

## 3. Primitive-identity theorems

### T-PI-1 — Primitive identity unicity theorem
Under one active evaluation context there exists exactly one governing primitive identity.

### T-PI-2 — Primitive identity compatibility theorem
Lawful evaluation is possible only if the active primitive identity is compatible with the object model, verdict universe, law line, canonicalization regime where required, and verification/admission semantics.

### T-PI-3 — Primitive identity preservation theorem
Any realization claiming full primitive conformance must preserve the same primitive identity semantics.

---

## 4. Scope theorems

### T-SC-1 — Admission-boundary scope theorem
BCF Primitive One is a deterministic, fail-closed, verifier-backed, closed-world admission boundary and not a broader universal reasoning engine.

### T-SC-2 — Non-truth theorem
No theorem of the primitive line entails that `ALLOW` establishes open-world truth.

### T-SC-3 — Non-universal-safety theorem
No theorem of the primitive line entails universal downstream safety.

### T-SC-4 — Verification-boundedness theorem
Verification establishes only lawful boundary fitness, not universal trust certification.

### T-SC-5 — Permit-boundedness theorem
Permit establishes only bounded positive release authority.

---

## 5. Object-model theorems

### T-OM-1 — Closed object-universe theorem
All normative primitive authority is carried only by object families explicitly defined by the object model or lawful revision thereof.

### T-OM-2 — Object-role determinacy theorem
Every normative object instance participating in primitive authority has exactly one principal normative role in the relevant context.

### T-OM-3 — Structural/semantic validity distinction theorem
Structural validity is not sufficient for lawful normative object validity.

### T-OM-4 — Binding necessity theorem
Where binding is required, absence, conflict, or ambiguity of that binding invalidates the object for its role.

### T-OM-5 — No implicit authority theorem
No normative object acquires positive authority by mere presence, naming, or external assumption.

---

## 6. Canonicalization theorems

### T-C14N-1 — Canonicalization determinism theorem
For every lawfully canonicalizable identity-relevant object under a fixed family, scope, and regime, exactly one canonical byte representation exists.

### T-C14N-2 — Canonicalization idempotence theorem
Reapplication of canonicalization to an already canonical representation does not change canonical identity.

### T-C14N-3 — Canonical uniqueness theorem
No two distinct outputs may both count as lawful canonical forms for the same object under the same regime.

### T-C14N-4 — Anti-ambiguity theorem of canonicalization
If multiple materially different identity-bearing interpretations remain possible and no lawful deterministic resolution exists, canonicalization fails.

### T-C14N-5 — Anti-invention theorem of canonicalization
Canonicalization cannot lawfully introduce authority-bearing content absent from the source object under the active regime.

### T-C14N-6 — Anti-improper-collapse theorem
Materially different identity-relevant objects must not collapse into the same canonical identity.

### T-C14N-7 — Canonical-identity derivation theorem
Where identity matters, canonical identity derives from canonical form.

### T-C14N-8 — Canonicalization-failure fail-closed theorem
Where canonical identity is required for admission-relevant evaluation, canonicalization failure blocks lawful `ALLOW`.

---

## 7. Verification theorems

### T-VF-1 — Binary verification theorem
Final verification judgment is exactly one of `VERIFIED` or `NOT_VERIFIED`.

### T-VF-2 — Verification biconditional theorem
`Verify(P, B) = VERIFIED` iff all necessary verification predicates jointly hold.

### T-VF-3 — Verification necessity-for-allow theorem
If `Verify(P, B) ≠ VERIFIED`, then `Admit(P, B, R) ≠ ALLOW`.

### T-VF-4 — Manifest-blocking theorem
Invalid manifest, missing required declared content, forbidden undeclared content, and content-binding mismatch block lawful verification where required by the line.

### T-VF-5 — Verification ambiguity-blocking theorem
Unresolved verification-relevant ambiguity blocks lawful verification.

### T-VF-6 — Verification replay theorem
Replay-equivalent canonical bundles preserve the same verification verdict.

### T-VF-7 — Verification no-warning-substitution theorem
Verification blockers may not be downgraded to warning-only while preserving lawful `VERIFIED`.

---

## 8. Admission theorems

### T-AD-1 — Binary admission theorem
Final admission verdict is exactly one of `{ALLOW, REFUSAL}`.

### T-AD-2 — Admission biconditional theorem
`ALLOW` iff all necessary admission predicates jointly hold under the active line.

### T-AD-3 — Necessary-condition theorem of admission
Every required admission conjunct is individually necessary for lawful `ALLOW`.

### T-AD-4 — Joint sufficiency theorem of admission
The full conjunction of required admission predicates is jointly sufficient for lawful `ALLOW`.

### T-AD-5 — Anti-silence theorem
Absence of detected error is not sufficient for lawful `ALLOW`.

### T-AD-6 — Closed-world admission theorem
Only explicit law-governed objects, structures, bindings, and relations may support lawful `ALLOW`.

### T-AD-7 — Ambiguity-blocking theorem of admission
Unresolved admission-relevant ambiguity without lawful deterministic disambiguation blocks lawful `ALLOW`.

### T-AD-8 — Non-compensation theorem
Failure of one necessary admission layer is not cancelled by strength in another unless lawfully defined by the active line.

---

## 9. Fail-closed theorems

### T-FC-1 — Global fail-closed theorem
Every admission-relevant failure, invalidity, incompleteness, contradiction, or unresolved ambiguity lands in final negative boundary behavior rather than permissive positive authority.

### T-FC-2 — Error-to-refusal theorem
At the final primitive boundary, admission-relevant error is observationally realized as `REFUSAL`, not a third verdict.

### T-FC-3 — Hidden-authority blocker theorem
If lawful positive authority would depend on unstated hidden authority-bearing material, lawful `ALLOW` is impossible.

### T-FC-4 — Incompleteness blocker theorem
If lawful `ALLOW` would require missing mandatory information, the result is fail-closed `REFUSAL`.

### T-FC-5 — Verification-failure landing theorem
Every verification failure blocks `ALLOW` and contributes to final fail-closed negative landing.

### T-FC-6 — Canonicalization-failure landing theorem
Every admission-relevant canonicalization failure blocks `ALLOW` and contributes to final fail-closed negative landing.

---

## 10. Refusal-algebra theorems

### T-RA-1 — Refusal completeness theorem
For every admission-blocking failure condition there exists a lawful refusal realization.

### T-RA-2 — No uncoded blocker theorem
No admission-blocking failure may remain outside the lawful refusal class/code universe.

### T-RA-3 — Verdict coherence theorem of refusal
Every lawful refusal carries verdict identity `REFUSAL`.

### T-RA-4 — Refusal class/code coherence theorem
Every lawful refusal code belongs to a lawful refusal class and is semantically coherent with it.

### T-RA-5 — Refusal binding theorem
Every lawful refusal is attributable to its relevant canonical decision context under lawful scope.

### T-RA-6 — Refusal replay-attribution theorem
Where replay is required, lawful refusal remains stably attributable across replay-equivalent environments.

### T-RA-7 — Deterministic refusal-classification theorem
For the same canonical context and blocker state, lawful refusal meaning is determinate.

### T-RA-8 — Multi-failure primary-refusal theorem
Where multiple admission blockers coexist, the active line determines a lawful primary refusal meaning.

### T-RA-9 — Anti-free-form refusal theorem
Free-form denial text without lawful refusal structure is not a sufficient refusal realization.

---

## 11. Permit-algebra theorems

### T-PA-1 — Permit completeness theorem
For every lawful admitted context, there exists a lawful permit realization.

### T-PA-2 — No unstructured positive remainder theorem
No lawful positive authority may remain only as raw success, opaque state, or free-form approval text where permit realization is required.

### T-PA-3 — Verdict coherence theorem of permit
Every lawful permit carries verdict identity `ALLOW`.

### T-PA-4 — Permit binding theorem
Every lawful permit is attributable to its relevant canonical admitted context under lawful scope.

### T-PA-5 — Action-authority theorem
Every lawful permit carries determinate, contract-compatible, non-ambiguous positive action-release meaning where applicable.

### T-PA-6 — Permit replay-attribution theorem
Where replay is required, lawful permit remains stably attributable across replay-equivalent environments.

### T-PA-7 — Deterministic permit-realization theorem
For the same canonical admitted context, lawful permit meaning is determinate.

### T-PA-8 — Positive-authority minimality theorem
A lawful permit carries no more and no less authority than the admitted context lawfully supports.

### T-PA-9 — Anti-free-form permit theorem
Free-form success text without lawful permit structure is not a sufficient permit realization.

---

## 12. Determinism and replay theorems

### T-DET-1 — Final-verdict determinism theorem
For the same canonical evaluation context under the same line, final verdict is the same.

### T-DET-2 — Verification determinism theorem
For the same canonical bundle under the same line, verification verdict is the same.

### T-DET-3 — Canonicalization determinism theorem
For the same lawfully canonicalizable object under the same family, scope, and regime, canonical output is the same.

### T-DET-4 — Refusal determinism theorem
For the same canonical blocker state, lawful refusal meaning is the same.

### T-DET-5 — Permit determinism theorem
For the same canonical admitted context, lawful permit meaning is the same.

### T-RP-1 — Replay verdict theorem
Replay-equivalent canonical contexts preserve the same final verdict.

### T-RP-2 — Replay verification theorem
Replay-equivalent canonical bundles preserve the same verification verdict.

### T-RP-3 — Replay refusal theorem
Replay-equivalent blocker contexts preserve the same lawful refusal meaning where required.

### T-RP-4 — Replay permit theorem
Replay-equivalent admitted contexts preserve the same lawful permit meaning where required.

### T-RP-5 — Replay anti-hidden-context theorem
If boundary meaning depends on hidden discretionary context not lawfully represented, replay-equivalent lawful meaning is violated.

---

## 13. No-bypass and equivalence theorems

### T-NB-1 — Official positive-path theorem
The official positive path is `SourceProfile -> AdmissionBundle -> Verification -> AdmissionEvaluation -> Permit -> ReleasedActionDescriptor` in normative effect.

### T-NB-2 — No lawful positive bypass theorem
No positive authority equivalent to lawful `ALLOW` may arise outside the official positive path.

### T-NB-3 — Verification-bypass impossibility theorem
No lawful `ALLOW` may arise by bypassing required verification.

### T-NB-4 — Permit-bypass impossibility theorem
Where permit realization is required, no lawful positive release authority may arise without lawful permit realization.

### T-EQ-1 ... T-EQ-10
Full primitive equivalence requires preservation of primitive identity, verdict universe, admission, verification, canonicalization, refusal, permit, fail-closed behavior, no-bypass behavior, and replay-equivalent meaning.

---

## 14. Impossibility theorems

The line commits at minimum to the following impossibility claims:
- no third final verdict
- no allow without verification
- no allow through unresolved ambiguity
- no permit without lawful admission
- no lawful refusal outside refusal algebra
- no canonical identity from guesswork
- no hidden positive authority
- no unrestricted permit
- no universal-truth theorem
- no universal-safety theorem

---

## 15. Closure target theorems

A strongly closed primitive line must eventually demonstrate:
- law-line closure
- object-model closure
- admission closure
- verification closure
- output closure
- canonical-identity closure
- primitive-equivalence closure
- executable-adequacy target theorem

These are the closure targets for later proof and mechanization.

---

## 16. Final theorem-set law statement

The theorem set of BCF Primitive One is the closed ledger of law-level propositions that define what must hold of the primitive across identity, scope, object model, canonicalization, verification, admission, refusal, permit, determinism, replay, fail-closed behavior, no-bypass discipline, equivalence, and impossibility boundaries, such that a realization is fully conformant only if these theorems are preserved together under the active law line and no hidden premise, semantic drift, permissive weakening, or scope inflation is used to satisfy them; accordingly, these theorem statements are the exact closure targets against which later proofs, mechanizations, executable adequacy arguments, corpora, and independent audits must be judged.

That is the theorem set.
