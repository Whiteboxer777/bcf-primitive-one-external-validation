# `SPEC/CANONICALIZATION_LAW.md`

## 0. Status

This document is the normative canonicalization-law specification for **BCF Primitive One**.
It defines how identity-relevant normative objects are reduced to canonical form, what canonical form means, which objects require canonicalization, what properties canonicalization must satisfy, what failures are canonicalization failures, and how identity, equality, manifest binding, and replay depend on canonicalization.

---

## 1. Purpose

Canonicalization exists so that authority does not rest on unstable, informal, or multiply-interpretable representation.
It is required for:
- stable identity
- deterministic replay
- stable manifest binding
- stable content binding
- stable request identity
- stable permit/refusal traceability
- implementation equivalence

Canonicalization is a law, not a convenience.

---

## 2. Scope

Every identity-relevant normative object family is governed by this law, including at minimum:
- `PrimitiveIdentity`
- `AdmissionBundle`
- `Manifest`
- `ManifestEntry`
- `BundleContentBinding`
- `AdmissionContract`
- `Request`
- `ActionDescriptor`
- `Witness` where identity matters
- `VerificationResult` where replay depends on identity
- `Permit`
- `Refusal`
- `ReplayBinding`
- `CanonicalIdentityRecord`

---

## 3. Core stance

Canonicalization is:
- deterministic
- idempotent
- closed-world
- anti-ambiguity
- identity-preserving
- fail-closed where identity is admission-relevant
- normatively prior to identity derivation
- normatively binding for replay and equality

---

## 4. Canonicalization function

For each identity-relevant object family `X`, there must exist a canonicalization regime and canonicalization function:

`c14n_X : X -> U`

where `U` is the finite byte-string universe.

Canonicalization is total over the lawful canonicalizable domain and fail-closed outside it.

---

## 5. Semantic functions of canonicalization

Canonicalization serves five principal functions:
1. identity derivation
2. equality stabilization
3. collapse of semantically irrelevant representation variance
4. replay stability
5. binding and hashing stability

---

## 6. Core axioms

### Determinism axiom
For a given family, regime, and lawful input object, canonicalization always produces the same canonical bytes.

### Idempotence axiom
Reapplication of canonicalization does not change canonical identity.

### Uniqueness axiom
For any lawful object under a given family and regime, there exists exactly one canonical representation.

### Anti-ambiguity axiom
If multiple materially different identity-bearing interpretations remain possible and no deterministic law-governed resolution exists, canonicalization fails.

### Stability axiom
Canonicalization preserves identity-relevant normative meaning.

### Non-expansion axiom
Canonicalization must not invent authority-bearing content, guessed defaults, or hidden environment-derived values.

### Scope axiom
Canonicalization is always interpreted under explicit family, role, bundle/local/global, and law-line scope where relevant.

---

## 7. Canonical identity derivation law

Where identity matters:
1. determine lawful family and scope
2. apply the active canonicalization regime
3. obtain canonical byte representation
4. derive identity from canonical form

Identity must not be derived directly from arbitrary source formatting, incidental field order, whitespace, serializer choice, or machine-local artifacts.

---

## 8. Manifest and bundle implications

Manifest semantics rely on canonicalization because manifest entries bind canonical content identity.

If actual content, after lawful canonicalization, does not match the identity implied or declared by the manifest, manifest satisfaction fails.

If required manifest-bound content cannot be lawfully canonicalized where canonical binding is required, positive verification is impossible.

---

## 9. Request, bundle, and output implications

### Request
Request identity must derive from canonical request form. Ambiguous request identity blocks lawful `ALLOW`.

### Bundle
Bundle identity must be canonically fixed. Canonicalization must preserve required-vs-optional and declared-vs-undeclared membership distinctions.

### Outputs
Permit and refusal identity must be canonically stable where replay, audit, or equivalence require it.
Canonicalization of outputs must not change verdict meaning or invent new authority.

---

## 10. Failure classes

Canonicalization failure occurs when:
- the object cannot be lawfully recognized as belonging to the required family
- structural prerequisites fail
- semantically relevant ambiguity remains unresolved
- identity-relevant contradictions remain unresolved
- the regime is missing, inconsistent, or inapplicable
- canonical output is not uniquely determined
- canonicalization would require unlawful invention or guesswork

Where canonical identity is required for admission-relevant evaluation, such failure blocks lawful `ALLOW` and collapses fail-closed.

No permissive fallback such as raw-source comparison, best-effort guessing, or arbitrary serializer choice is lawful where canonical identity is required.

---

## 11. Determinism, replay, and equivalence

Equal canonical inputs under the same regime must yield the same canonical outputs across conforming replay-capable environments.

Two implementations can be primitive-equivalent only if their canonicalization behavior is equivalent for all identity-relevant objects under the same active regime.

Implementations are non-equivalent if they differ in whether:
- an object is lawfully canonicalizable
- a canonical identity is assigned
- ambiguity is rejected
- distinct authority-bearing objects improperly collapse
- replay-stable identity is preserved

---

## 12. Theorem commitments

The line commits at minimum to:
- deterministic canonicalization theorem
- idempotence theorem
- anti-ambiguity theorem
- anti-invention theorem
- anti-improper-collapse theorem
- manifest-binding theorem
- replay-stability theorem
- fail-closed canonicalization theorem
- regime-compatibility theorem

---

## 13. Final canonicalization-law statement

In BCF Primitive One, canonicalization is the law-governed deterministic reduction of each identity-relevant normative object, under an explicit or lawfully fixed object-family-and-scope-specific regime, to exactly one canonical byte representation from which canonical identity is derived, such that semantically irrelevant representational variance is collapsed, identity-relevant meaning is preserved, repeated canonicalization is idempotent in normative effect, materially different authority-bearing objects do not collapse improperly, unresolved identity-relevant ambiguity or structural invalidity causes canonicalization failure, and every admission-relevant canonicalization failure collapses fail-closed so that no lawful positive authority may arise from non-canonical, ambiguously canonical, guessed, unstable, or regime-incompatible representation.

That is the canonicalization law.
