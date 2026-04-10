# `SPEC/ADMISSION_SEMANTICS.md`

## 0. Status

This document is the normative admission-semantics specification for **BCF Primitive One**.
It defines what admission means, how verification and request-conformance participate in the judgment, what `ALLOW` and `REFUSAL` mean, which conditions are necessary and jointly sufficient, and how failures collapse into refusal.

---

## 1. Purpose of admission semantics

Admission answers exactly this question:

> given a candidate request and a candidate admission bundle under the active primitive law, does the request lawfully pass the bundle-bound admission boundary and yield a lawful permit for release of the bound action descriptor, or does it not?

The answer space is exactly:
- `ALLOW`
- `REFUSAL`

Admission is:
- closed-world
- deterministic
- fail-closed
- non-probabilistic
- binding-sensitive
- anti-ambiguity unless lawfully resolved

---

## 2. What admission is not

Admission is not:
- truth
- mere parsing
- mere absence of detected error
- broad policy rhetoric
- universal legality
- universal safety

Admission is contract-bound passability under a verified boundary.

---

## 3. Semantic domain of admission

Admission is a judgment over a normative evaluation configuration containing at minimum:
1. active `PrimitiveIdentity`
2. candidate `AdmissionBundle`
3. candidate `Request`
4. bundle-bound `AdmissionContract`
5. all mandatory identity, manifest, verification, binding, and replay relations required by the law line

No lawful admission judgment exists over a request in isolation.

---

## 4. Admission judgment form

Canonical form:

`Admit(P, B, R) ∈ {ALLOW, REFUSAL}`

where `P` is primitive identity, `B` is candidate bundle, and `R` is candidate request.

---

## 5. Meaning of `ALLOW`

`ALLOW` means:
> under the active primitive law, the candidate request lawfully passes the candidate bundle-bound admission boundary and yields a lawful permit bound to the canonical bundle, the canonical request, and the bound action descriptor.

A lawful `ALLOW` entails all of the following simultaneously:
1. valid primitive identity
2. valid normative bundle
3. satisfied bundle manifest and content bindings
4. required bundle content present and identity-consistent
5. successful bundle verification
6. valid request object
7. satisfied request shape constraints
8. satisfied request bounds constraints
9. satisfied admission contract conditions
10. compatible action-release meaning where applicable
11. no admission-relevant ambiguity remains
12. no fail-closed trigger occurs
13. lawful permit can be realized

`ALLOW` does not mean external-world success, universal legality, or universal correctness.

---

## 6. Meaning of `REFUSAL`

`REFUSAL` means:
> under the active primitive law, the candidate request does not lawfully pass the candidate bundle-bound admission boundary, and no lawful permit may be produced for release of the bound action descriptor in that evaluation context.

`REFUSAL` is mandatory whenever lawful `ALLOW` cannot be established.

`REFUSAL` does not mean global falsehood or permanent impossibility in every future context.

---

## 7. Binary closure of admission

Admission has exactly two final outcomes:
- `ALLOW`
- `REFUSAL`

No final state such as maybe, partial pass, warning-only, provisional allow, or inconclusive exists.

Where lawful `ALLOW` cannot be fully established, the result is `REFUSAL`.

---

## 8. Primitive-level semantic predicates

The following predicates define lawful admission.

### `PrimitiveValid(P)`
The primitive identity is valid, unambiguous, law-line compatible, and verdict-universe compatible.

### `BundleValid(B)`
The candidate bundle is a valid `AdmissionBundle`, identity-stable, manifest-bound, contract-bearing, and non-contradictory.

### `ManifestSatisfied(B)`
Manifest is valid; required declared content is present; declared and actual identity-relevant content match; forbidden undeclared content is absent where the line forbids it.

### `VerificationSucceeded(B)`
The bundle has been lawfully verified and no required verification claim remains unsatisfied.

### `RequestValid(R, B)`
`R` parses as a request object, is interpretable under the active bundle/contract context, and contains no forbidden or ambiguous authority-bearing structure.

### `ShapeSatisfied(R, B)`
`R` conforms to the contract-bound request shape.

### `BoundsSatisfied(R, B)`
`R` lies within all required admitted bounds under a clear comparison regime.

### `ContractSatisfied(R, B)`
All contract conditions required for positive passage hold, and no contract-level prohibition is violated.

### `ActionBindingSatisfied(R, B)`
Where action release is governed, the request’s positive outcome is bound to a determinate lawful action-release meaning.

### `WitnessSatisfied(R, B)`
All required witness/support relations hold where required.

### `NoFailClosedTrigger(P, B, R)`
No admission-relevant fail-closed condition has occurred.

---

## 9. Main biconditional

`Admit(P, B, R) = ALLOW`

iff all of the following hold:
1. `PrimitiveValid(P)`
2. `BundleValid(B)`
3. `ManifestSatisfied(B)`
4. `VerificationSucceeded(B)`
5. `RequestValid(R, B)`
6. `ShapeSatisfied(R, B)`
7. `BoundsSatisfied(R, B)`
8. `ContractSatisfied(R, B)`
9. `ActionBindingSatisfied(R, B)` where required
10. `WitnessSatisfied(R, B)` where required
11. `NoFailClosedTrigger(P, B, R)`

Otherwise:
`Admit(P, B, R) = REFUSAL`

This biconditional is the central semantic law of admission.

---

## 10. Necessity and sufficiency

- Each predicate above is individually necessary for lawful `ALLOW`.
- Their full conjunction is jointly sufficient for lawful `ALLOW`.
- A conforming implementation may not add hidden extra positive conditions.
- A conforming implementation may not weaken any required condition.

---

## 11. Failure collapse

At minimum, the following collapse to refusal:
- primitive identity failure
- bundle invalidity
- manifest failure
- verification failure
- request invalidity
- request shape failure
- request bounds failure
- contract non-conformance
- action binding failure
- required witness failure
- unresolved ambiguity
- hidden-authority dependence
- inability to establish lawful `ALLOW`

Diagnostics may exist, but they do not create a third verdict.

---

## 12. Ambiguity and unknowns

Admission-relevant ambiguity yields refusal unless the active law provides a deterministic disambiguation rule.
Unknown authority-bearing structure cannot positively support admission.
Unstated environmental assumptions cannot manufacture `ALLOW`.

---

## 13. Verification relation

Verification is semantically upstream of `ALLOW`.
A request cannot compensate for an invalid boundary object.
If `Verify(P, B) = NOT_VERIFIED`, then `Admit(P, B, R) ≠ ALLOW` for every candidate request under `B`.

---

## 14. Action-boundedness

`ALLOW` is not semantically complete until what is being authorized for release is fixed. Where the primitive instance governs action release, lawful `ALLOW` is tied to a bound action-release meaning.

If materially different action-release meanings remain possible and no lawful deterministic resolution exists, lawful `ALLOW` is impossible.

---

## 15. Determinism and replay

Equal canonical inputs under the same law line yield the same verdict class.
No hidden or discretionary state may affect lawful admission meaning.
Replay of the same canonical bundle/request pair under the same law line must preserve the same verdict class.

---

## 16. Theorem commitments

The admission line commits at minimum to:
- binary admission theorem
- verification necessity theorem
- conjunctive admissibility theorem
- fail-closed collapse theorem
- anti-silence theorem
- closed-world theorem
- deterministic replay theorem
- action-boundedness theorem
- anti-guessing theorem

---

## 17. Final semantic law statement

In BCF Primitive One, admission is the deterministic, fail-closed, closed-world semantic judgment that a canonical request, under a canonical verified admission bundle and its bound admission contract, lawfully passes the boundary and yields a lawful permit bound to the request, bundle, and action-release meaning; this judgment yields `ALLOW` if and only if all primitive-validity, bundle-validity, manifest, verification, request-validity, shape, bounds, contract, action-binding, witness, and no-fail conditions required by the active law line jointly hold, and yields `REFUSAL` in every other case, including every case of invalidity, incompleteness, ambiguity, mismatch, or inability to lawfully establish positive passage.

That is the admission semantics.
