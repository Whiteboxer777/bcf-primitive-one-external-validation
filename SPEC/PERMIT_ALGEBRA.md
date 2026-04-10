# `SPEC/PERMIT_ALGEBRA.md`

## 0. Status

This document is the normative permit-algebra specification for **BCF Primitive One**.
It defines the structure, semantics, binding rules, identity rules, determinism rules, and equivalence criteria of permit as the positive output family of the primitive.

---

## 1. Purpose

The permit algebra exists to ensure that lawful `ALLOW` is realized as:
1. a normative positive object family, not an unstructured success bit
2. an authority bound to the exact canonical decision context that produced it
3. an explicit, typed, and non-ambiguous positive meaning
4. a determinate action-release meaning where the primitive instance governs release
5. a replay-attributable positive object where required
6. a bounded authority surface rather than vague approval

Permit is the structured realization of lawful positive authority.

---

## 2. Core domains

Let:
- `A` be the domain of canonical admitted contexts
- `T` be the domain of lawful action-release targets
- `PObj` be the domain of lawful permit objects
- `PB` be the domain of lawful permit bindings
- `PScope` be the domain of permit scopes

The permit algebra requires a lawful realization relation:

`π : A -> PObj`

factoring semantically through:
- `β_permit : A -> PB`
- `τ_action : A -> T`

---

## 3. Permit-object form

A lawful permit object must semantically realize at least:

`Permit = (primitive_identity, verdict_identity, permit_binding, action_authority, replay_binding, permit_scope, permit_identity)`

Mandatory semantics:
- verdict identity = `ALLOW`
- primitive identity
- permit binding
- action authority
- replay binding where required
- permit scope
- permit identity where the line requires identity-bearing permit outputs

Optional descriptive or diagnostic text is non-authoritative.

---

## 4. Permit binding

Every lawful permit must be attributable to the relevant positive decision context through a lawful permit binding connecting, where applicable:
- primitive identity
- canonical bundle identity
- canonical request identity
- contract scope
- action descriptor identity or release-target identity
- authority scope needed to interpret the permit lawfully

Permit binding must be context-attributable, non-ambiguous, action-coherent, replay-compatible, and verdict-coherent.

---

## 5. Action authority

`ALLOW` is not abstract success. It is authorization to release a bound action descriptor or equivalent release target under the active line.

For a lawful permit, action authority must be:
- bound
- non-ambiguous
- contract-compatible
- context-compatible
- scope-bounded

No lawful permit may silently widen positive authority beyond what the admitted context supports.

---

## 6. Permit identity and replay

Where replay, audit, or downstream binding require it, permit must have stable canonical identity.

Permit identity must be:
- canonically derivable where required
- scope-aware
- binding-coherent
- stable across replay-equivalent admitted contexts where the line requires identity-bearing permits

Replay-binding must be sufficient to re-identify the canonical admitted context in principle without hidden discretionary data.

---

## 7. Completeness law

For every canonical admitted context, there exists at least one lawful permit realization.

There must be no lawful positive authority that remains only as:
- raw boolean success
- opaque internal state
- free-form approval text
- process continuation without lawful permit realization where the line requires it

---

## 8. Exclusivity and determinism

For a given canonical evaluation context, final verdict identity cannot be both `ALLOW` and `REFUSAL`.

For a fixed canonical admitted context, permit meaning must be determinable under the active line.
Implementations may not arbitrarily choose among incompatible permit meanings for the same admitted context.

---

## 9. Ambiguity, hidden state, and no widening

If the system cannot determine which permit meaning lawfully applies because the positive context itself is materially ambiguous and no lawful disambiguation exists, then no lawful permit may arise; the admission boundary must already have collapsed to `REFUSAL`.

Permit meaning must not depend on hidden internal state not attributable to the admitted context where replay-equivalent meaning is required.

Permit must carry no more and no less authority than the admitted context lawfully supports.

---

## 10. Relation to admission and no-bypass

A permit may lawfully exist only if the admitted context satisfies the full admission biconditional.
There is no lawful permit for partially satisfied or only-apparently-satisfied admission.

Within the normative boundary, no positive authority equivalent to lawful `ALLOW` exists outside the official positive path and lawful permit realization where permit realization is required.

---

## 11. Invariants

Every lawful permit satisfies:
- verdict invariant (`ALLOW`)
- binding invariant
- action-authority invariant
- replay invariant where required
- completeness invariant
- determinism invariant
- non-overreach invariant
- binary exclusivity invariant

---

## 12. Theorem commitments

The line commits at minimum to:
- permit completeness theorem
- no unstructured positive remainder theorem
- verdict coherence theorem
- binding theorem
- action-authority theorem
- replay-attribution theorem
- deterministic realization theorem
- positive-authority minimality theorem
- no positive bypass theorem
- anti-free-form theorem

---

## 13. Final permit-algebra law statement

In BCF Primitive One, permit is the structured positive realization of the final verdict `ALLOW`, defined over a closed algebra in which every canonically admitted evaluation context projects, by law-governed realization and binding rules, to a lawful permit object carrying the active primitive identity, verdict identity, lawful permit binding to the canonical bundle/request/admission context, determinate and contract-compatible positive action-release authority where the primitive instance governs action release, lawful scope, and replay-stable attribution where required; this algebra is complete over lawful positive admission space, deterministic for canonical equivalent admitted contexts, closed against ad hoc or free-form positive authority, exact in the sense that it carries no less and no more authority than the admitted context lawfully supports, and exclusive in the sense that no equivalent positive authority may arise outside the official positive path and its lawful permit realization.

That is the permit algebra.
