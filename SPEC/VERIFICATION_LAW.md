# `SPEC/VERIFICATION_LAW.md`

## 0. Status

This document is the normative verification-law specification for **BCF Primitive One**.
It defines what verification is, what it operates over, what counts as verification success or failure, how verification relates to admissibility, what exact verification predicates are required, and what later implementations must preserve.

---

## 1. Purpose of verification

Verification answers this boundary-directed question:

> is the candidate admission bundle lawfully valid, identity-stable, content-bound, and fit to serve as the normative admission boundary under the active primitive law?

Verification concerns the boundary object. It is distinct from request admissibility.

Thus:
- verification = boundary validity judgment
- admission evaluation = request passability judgment under a verified boundary

Verification is necessary but not sufficient for `ALLOW`.

---

## 2. What verification is not

Verification is not:
- open-ended trust rhetoric
- request admissibility
- mere existence check
- optional pre-processing
- broad legal or hardware assurance by itself

---

## 3. Verification judgment form

Canonical judgment:

`Verify(P, B) ∈ {VERIFIED, NOT_VERIFIED}`

where `P` is active primitive identity and `B` is candidate bundle.

This is separate from the final primitive verdict universe.
At the primitive boundary:
- `VERIFIED` is necessary for `ALLOW`
- `NOT_VERIFIED` blocks `ALLOW`
- failure to establish verification collapses to final `REFUSAL`

---

## 4. Meaning of `VERIFIED`

`VERIFIED` means:
> under the active primitive law, the candidate bundle has been lawfully established as a valid, identity-stable, content-bound, non-ambiguous admission boundary object fit to serve as the boundary under which request admissibility may be judged.

A lawful `VERIFIED` result entails all of the following:
1. valid and applicable primitive identity
2. valid candidate `AdmissionBundle`
3. structurally valid bundle
4. lawfully canonicalizable identity where required
5. valid manifest where required
6. satisfied declared content relations
7. required bundle content present
8. forbidden undeclared content absent where the line closes content membership
9. satisfied content-binding relations
10. absence of unresolved verification-relevant ambiguity
11. satisfied witness/support relations where verification requires them
12. satisfied verification claims
13. absence of verification fail-closed triggers

---

## 5. Meaning of `NOT_VERIFIED`

`NOT_VERIFIED` means:
> under the active primitive law, the candidate bundle has not been lawfully established as a valid, identity-stable, content-bound, non-ambiguous admission boundary object fit to serve as the admission boundary.

It arises from at least one of:
- primitive incompatibility
- bundle invalidity
- identity/canonicalization failure where required
- manifest invalidity
- missing required content
- forbidden undeclared content
- content-binding mismatch
- unsatisfied verification claim
- required witness/support failure
- unresolved ambiguity
- any verification fail-closed trigger
- inability to establish lawful `VERIFIED`

---

## 6. Necessary verification predicates

### `PrimitiveApplicable(P, B)`
The active primitive identity lawfully governs verification of the candidate bundle.

### `BundleCandidateValid(B)`
`B` is a structurally and semantically valid candidate `AdmissionBundle`.

### `BundleCanonicalizable(B)`
All verification-relevant identity can be lawfully canonicalized and uniquely fixed.

### `ManifestValid(B)`
The manifest exists where required, is structurally valid, attributable to the target bundle, and non-ambiguous.

### `RequiredContentPresent(B)`
All required declared content is present.

### `NoForbiddenUndeclaredContent(B)`
No undeclared content exists where the line forbids it.

### `ContentBindingsSatisfied(B)`
Declared content and actual canonical content identity match lawfully.

### `VerificationClaimsSatisfied(P, B)`
All required verification claims hold.

### `VerificationWitnessSatisfied(P, B)`
All verification-required witness/support relations hold where required.

### `NoVerificationAmbiguity(P, B)`
No verification-relevant ambiguity remains unresolved.

### `NoVerificationFailClosedTrigger(P, B)`
No verification-relevant fail-closed blocker has occurred.

---

## 7. Main biconditional

`Verify(P, B) = VERIFIED`

iff all of the following hold:
1. `PrimitiveApplicable(P, B)`
2. `BundleCandidateValid(B)`
3. `BundleCanonicalizable(B)`
4. `ManifestValid(B)` where required
5. `RequiredContentPresent(B)`
6. `NoForbiddenUndeclaredContent(B)` where applicable
7. `ContentBindingsSatisfied(B)`
8. `VerificationClaimsSatisfied(P, B)`
9. `VerificationWitnessSatisfied(P, B)` where required
10. `NoVerificationAmbiguity(P, B)`
11. `NoVerificationFailClosedTrigger(P, B)`

Otherwise:
`Verify(P, B) = NOT_VERIFIED`

---

## 8. Necessary/sufficient relation

- Each predicate above is individually necessary for lawful `VERIFIED`.
- Their conjunction is jointly sufficient for lawful `VERIFIED`.
- No implementation may add hidden extra positive verification conditions while claiming unchanged semantics.
- No implementation may weaken a required verification condition.

---

## 9. Manifest/content consequences

Where manifest/content binding is part of the line:
- invalid manifest blocks `VERIFIED`
- missing required declared content blocks `VERIFIED`
- forbidden undeclared content blocks `VERIFIED`
- content-binding mismatch blocks `VERIFIED`

The manifest is not decorative metadata.

---

## 10. Canonicalization relation

Where verification depends on canonical identity, canonicalization is semantically upstream of verification success.
If the bundle cannot be lawfully canonicalized where verification depends on identity, `VERIFIED` is impossible.

No raw-source fallback is lawful where canonical identity is required.

---

## 11. Witness, ambiguity, and hidden-context rules

- Witness/support relations may be verification-relevant where the active line requires them.
- Witnesses do not override primitive law.
- Unresolved verification-relevant ambiguity blocks `VERIFIED`.
- Human guesswork, undocumented convention, or hidden environment state may not rescue positive verification.

---

## 12. Determinism and replay

For the same canonical bundle under the same primitive line and lawful regime, verification must yield the same result.
Replay-equivalent environments must preserve the same verification verdict.

---

## 13. Relation to admission

`Verify(P, B) = VERIFIED` is necessary for `Admit(P, B, R) = ALLOW`.
If `Verify(P, B) = NOT_VERIFIED`, then no request under `B` may lawfully yield `ALLOW`.
At the primitive boundary, verification failure collapses to final `REFUSAL`.

---

## 14. Theorem commitments

The line commits at minimum to:
- binary verification theorem
- verification biconditional theorem
- verification necessity-for-allow theorem
- manifest-blocking theorem
- ambiguity-blocking theorem
- deterministic verification theorem
- replay theorem for verification
- no-warning-substitution theorem
- boundary-fitness theorem

---

## 15. Final verification-law statement

In BCF Primitive One, verification is the deterministic, closed-world, fail-closed boundary-directed judgment that a candidate admission bundle, under the active primitive law and its compatible identity/canonicalization regime, has been lawfully established as a valid, identity-stable, manifest-satisfied, content-bound, non-ambiguous admission boundary object fit to govern subsequent request admissibility; this judgment yields `VERIFIED` if and only if all primitive-applicability, bundle-validity, canonicalizability, manifest-validity, required-content, forbidden-extra-content, content-binding, verification-claim, verification-witness, ambiguity-free, and no-fail predicates required by the active line jointly hold, and yields `NOT_VERIFIED` in every other case, including every case of invalidity, incompleteness, ambiguity, mismatch, or inability to lawfully establish bundle fitness as boundary, with the further law that no final `ALLOW` may arise from any bundle that is not lawfully `VERIFIED`.

That is the verification law.
