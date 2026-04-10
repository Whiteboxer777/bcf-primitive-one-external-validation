# `SPEC/PRIMITIVE_LAW.md`

## 0. Status

This document is the normative law sheet for **BCF Primitive One**.
It defines the primitive identity, object universe, admissibility laws, failure laws, canonicalization requirements, verdict semantics, binding requirements, and equivalence criteria that later implementations, verifiers, runners, proofs, tests, and release artifacts must satisfy.

Where later code, tests, bundles, manifests, verifiers, runners, or documentation conflict with this document, this document is the controlling source for the primitive identity.

---

## 1. Primitive identity

### Canonical name
**BCF Primitive One**

### Primitive class
**deterministic fail-closed verifier-backed admission primitive**

Mandatory class properties:
1. deterministic
2. fail-closed
3. verifier-backed
4. admission primitive

### Primitive role
**pre-action legitimacy/admission boundary**

### Short definition
BCF Primitive One is a closed, deterministic, fail-closed, verifier-backed mechanism that reduces a candidate request and a bound admission bundle to exactly one of two normative outcomes:
- `ALLOW`
- `REFUSAL`

`ALLOW` is possible only when the bundle is valid, verified, structurally bound, and the request is valid and contractually admissible under the bundle. All other cases reduce to `REFUSAL`.

---

## 2. Normative purpose and non-purpose

### Positive purpose
To determine whether a candidate request may normatively pass a canonical admission boundary and yield a bound permit for release of a bound action descriptor.

### Negative purpose
The primitive does not decide:
- truth
- intelligence
- optimization
- open-world correctness
- universal safety
- universal legality
- broad governance or compliance completeness

Admission is contract-bound passability, not open-world truth.

---

## 3. Scope anchor

The sole positive authority type of the primitive is:
> authority to determine whether a candidate request may pass the law-governed bundle-bound boundary and, if so, realize lawful permit for release of the bound action descriptor.

Everything else is outside scope unless explicitly added by lawful revision.

---

## 4. Normative universes

### Byte universe
Let `B = {0,1,...,255}` and `U = B*`.
All identity-relevant normative artifacts must be reducible to elements of `U`.

### Structured normative object universe
The primitive recognizes only the closed object families defined by `SPEC/OBJECT_MODEL.md`.

---

## 5. Core normative objects

The primitive normatively operates over:
- `PrimitiveIdentity`
- `SourceProfile`
- `AdmissionBundle`
- `Manifest`
- `VerificationResult`
- `Request`
- `Permit`
- `Refusal`
- `Witness`
- `ActionDescriptor`
- required binding families from the object model

No other object family may carry positive authority unless added by lawful revision.

---

## 6. Official positive path

The only normative positive route is:

`SourceProfile -> AdmissionBundle -> Verification -> AdmissionEvaluation -> Permit -> ReleasedActionDescriptor`

No alternate route may count as lawful positive authority.

Excluded as independent positive routes:
- request-to-action without bundle verification
- permissive fallback under uncertainty
- natural-language operator override
- warning-pass channels
- degraded allow states

---

## 7. Verdict universe

The final primitive verdict set is exactly:

`V = {ALLOW, REFUSAL}`

Excluded final verdicts:
- unknown
- maybe
- inconclusive
- warning-pass
- provisional-allow
- degraded-allow

Every candidate evaluation must terminate in exactly one element of `V`.

---

## 8. Totality law

For every candidate normative evaluation configuration recognized by the primitive, there exists exactly one final verdict in `V`.

Implementation-level partiality must collapse observationally into totality via fail-closed refusal.

---

## 9. Fail-closed law

Any admission-relevant defect, invalidity, mismatch, incompleteness, ambiguity, or failure must reduce to `REFUSAL`.

This includes, without limitation:
- parse failures
- canonicalization failures
- manifest failures
- missing required files
- forbidden undeclared content
- digest mismatches
- tamper evidence
- request shape invalidity
- request bounds failure
- contract mismatch
- verification failure
- witness inconsistency where required
- missing action binding where required
- unresolved ambiguity

No error channel may create positive authority.

---

## 10. Closed-world law

Only explicitly defined and admitted structures, declarations, bindings, and contract relations may support positive admission.

Unknown or unstated authority-bearing material is non-authoritative.
If positive admission would depend on it, the outcome must be `REFUSAL`.

---

## 11. Canonicalization law anchor

Each identity-relevant normative object must have exactly one canonical representation for identity, equality, manifest, and replay purposes.

Canonicalization must be:
- deterministic
- idempotent
- anti-ambiguity
- anti-invention
- fail-closed where admission-relevant

Identity must derive from canonical form, not arbitrary source formatting.

---

## 12. Manifest-binding law

An admission bundle is normatively valid only if its manifest binding is satisfied.
This entails:
- missing required declared file -> failure
- undeclared forbidden content -> failure
- tampered file content -> failure
- mismatched digest/binding -> failure

Manifest is part of the admission law, not decorative metadata.

---

## 13. Verification law anchor

Positive admission is impossible unless bundle verification succeeds.
Verification concerns at minimum:
- manifest integrity and conformance
- required content presence
- identity consistency
- tamper absence relative to normative bindings
- boundary-object structural validity
- witness consistency where required

Verification success is necessary but not sufficient for `ALLOW`.

---

## 14. Request-conformance law

A request may support positive admission only if it is:
- structurally valid
- shape-conformant
- within admitted bounds
- contractually conformant under the verified bundle
- free of unresolved authority-bearing ambiguity

Otherwise: `REFUSAL`.

---

## 15. Admission law

A candidate request under a candidate bundle yields `ALLOW` iff all admission conditions required by this primitive law are satisfied.

At minimum:
1. valid primitive identity
2. lawful reduction to a normative admission bundle
3. valid bundle structure
4. satisfied manifest binding
5. required bundle content present and identity-consistent
6. successful verification
7. valid request
8. shape satisfaction
9. bounds satisfaction
10. contract satisfaction
11. witness satisfaction where required
12. valid action binding where required
13. no fail-closed trigger

If any required condition fails: `REFUSAL`.

---

## 16. Refusal law anchor

`REFUSAL` is mandatory whenever the primitive cannot lawfully produce `ALLOW`.

No internal exception handler, warning mode, degraded mode, or compatibility mode may convert a refusal-triggering state into lawful `ALLOW`.

---

## 17. Permit law anchor

Every lawful positive output must be a structured permit bound at minimum to:
- primitive identity
- bundle identity
- request identity
- action descriptor identity or release-target binding
- replay-relevant identity where required

A permit is valid iff it is produced under lawful satisfaction of the admission law. There is no lawful unbound permit.

---

## 18. Determinism and replay

For equal canonical normative inputs under the same primitive law, the verdict must be equal.
Replay of the same canonical bundle/request pair under the same law line must yield the same verdict class.

No hidden discretionary state may affect lawful boundary meaning.

---

## 19. No-bypass law

Within the normative boundary of BCF Primitive One, there is no lawful positive bypass around the official positive path.

This is a primitive-level law, not by itself an OS or hardware guarantee.

---

## 20. Primitive-equivalence criterion

A realization belongs to BCF Primitive One only if it preserves together:
- verdict universe `{ALLOW, REFUSAL}`
- fail-closed semantics
- closed-world law
- canonical identity discipline
- manifest-binding consequences
- verification necessity
- admission biconditional
- permit/refusal meanings
- replay-equivalent behavior
- no-bypass behavior

Anything else is not the same primitive.

---

## 21. Minimal theorem commitments

The line commits at minimum to:
- verdict totality
- fail-closed safety
- closed-world admissibility
- canonicalization idempotence
- verification precondition
- deterministic replay
- permit binding
- refusal completeness
- no lawful positive bypass

The exact theorem ledger is fixed by `SPEC/THEOREM_SET.md`.

---

## 22. Final law statement

BCF Primitive One is a closed normative admission primitive whose lawful positive authority exists only when a canonically bound admission bundle has validly passed verification and a canonically bound request has validly satisfied the bundle-bound admission contract, such that the primitive deterministically yields a structured permit bound to the request, bundle, and action descriptor; in every other case, including every admission-relevant failure, ambiguity, mismatch, or incompleteness, the primitive must deterministically yield structured refusal.

That is the primitive law.
