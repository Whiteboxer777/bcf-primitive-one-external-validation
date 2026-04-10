# `SPEC/OBJECT_MODEL.md`

## 0. Status

This document is the normative object-model specification for **BCF Primitive One**.
It defines the full normative object universe recognized by the primitive, the object roles, required semantic fields, binding relations, validity conditions, identity conditions, and object-family invariants.

It is the **normative object constitution** of the primitive.

---

## 1. Object-model commitments

The object model is committed to:
- closed object-family discipline
- typed role discipline
- identity discipline
- binding discipline
- anti-implicitness discipline
- fail-closed object semantics

Only explicitly defined object families are normative.

---

## 2. Normative object universe

BCF Primitive One recognizes exactly the following principal normative object families:

1. `PrimitiveIdentity`
2. `SourceProfile`
3. `AdmissionBundle`
4. `Manifest`
5. `ManifestEntry`
6. `BundleContentBinding`
7. `VerificationResult`
8. `VerificationClaim`
9. `Request`
10. `RequestShape`
11. `RequestBounds`
12. `AdmissionContract`
13. `AdmissionCondition`
14. `Witness`
15. `WitnessBinding`
16. `ActionDescriptor`
17. `ActionBinding`
18. `Permit`
19. `PermitBinding`
20. `Refusal`
21. `RefusalCode`
22. `RefusalClass`
23. `ReplayBinding`
24. `CanonicalIdentityRecord`

No additional family may carry admission authority unless introduced by explicit revision.

---

## 3. General object axioms

### Role axiom
Every normative object instance must have exactly one principal normative role in a given evaluation context.

### Completeness axiom
A normative object is complete only if all semantics required for its role are present and non-ambiguous.

### Validity axiom
A normative object is valid for its role iff:
1. it belongs to a recognized family
2. it is structurally well-formed
3. it is semantically complete
4. its identity is stable where required
5. its bindings satisfy applicable laws

### Anti-ambiguity axiom
Role-ambiguous objects are invalid where authority depends on disambiguation.

### Binding axiom
If a family requires binding, absence, mismatch, or ambiguity of binding invalidates the object for its role.

### Non-authority axiom
No object acquires positive authority merely by being present in a tree, parser output, or memory.

---

## 4. Family definitions

### `PrimitiveIdentity`
Fixes which primitive line governs. Must unambiguously identify BCF Primitive One, its law line, object-model compatibility, and verdict-universe identity.

### `SourceProfile`
Source-side declarative object from which a canonical bundle is constructed. It is not itself the final authority-bearing boundary object.

### `AdmissionBundle`
The principal authority-bearing boundary object. It must bind primitive identity, manifest binding, admission contract, required content declarations, action-binding context where required, and replay-relevant identity support.

### `Manifest`
Declares and binds the identity-relevant contents of an admission bundle.

### `ManifestEntry`
Declares one identity-relevant content member of the bundle, including locus, role, identity-binding material, and requirement status.

### `BundleContentBinding`
Binds declared bundle content to actual canonical content identity.

### `AdmissionContract`
Defines the closed admissibility rules under which a request can or cannot pass.

### `AdmissionCondition`
One condition unit belonging to the admission contract whose satisfaction is required, relevant, or constraining for lawful admission.

### `RequestShape`
Defines the admissible structural form of a request.

### `RequestBounds`
Defines bounded limits that a request must satisfy to remain admissible.

### `VerificationClaim`
One verification-relevant claim that must hold for the bundle to count as verified.

### `VerificationResult`
Structured object representing the outcome of applying verification to the bundle.

### `Witness`
Supporting bound evidence, support state, or replay-relevant support material related to bundle, contract, or decision context. It does not override primitive law.

### `WitnessBinding`
Binds a witness to its lawful target and role.

### `Request`
The normative candidate input object seeking admission under a verified bundle.

### `ActionDescriptor`
Identifies the action target that a lawful permit authorizes for release.

### `ActionBinding`
Binds bundle or contract context to one or more permitted action descriptors under explicit conditions.

### `ReplayBinding`
Binds outputs or states back to canonical bundle/request identity for replay and audit.

### `PermitBinding`
Binds a permit to primitive, bundle, request, action descriptor, and replay context.

### `Permit`
Structured positive output object representing lawful successful admission.

### `RefusalCode`
Specific coded reason family or reason instance under which a refusal is classified.

### `RefusalClass`
Higher-level defect-family classification under which refusal codes are grouped.

### `Refusal`
Structured negative output object representing that lawful positive admission did not occur.

### `CanonicalIdentityRecord`
Binds an object instance to its canonical identity representation, including family, scope, regime, and derivation basis.

---

## 5. Object relation model

The core lawful relation graph is:

- `SourceProfile -> AdmissionBundle`
- `AdmissionBundle -> Manifest -> ManifestEntry -> BundleContentBinding`
- `AdmissionBundle -> AdmissionContract`
- `AdmissionContract -> AdmissionCondition`
- `AdmissionContract -> RequestShape`
- `AdmissionContract -> RequestBounds`
- `AdmissionContract -> ActionBinding`
- `AdmissionBundle -> VerificationClaim -> VerificationResult`
- `Witness -> WitnessBinding -> target`
- `Request -> AdmissionContract`
- `ALLOW -> Permit -> PermitBinding -> ActionDescriptor`
- `REFUSAL -> Refusal -> RefusalCode / RefusalClass`
- `VerificationResult / Permit / Refusal -> ReplayBinding -> canonical inputs`

---

## 6. Object admissibility relevance

### Authority-bearing objects
- `PrimitiveIdentity`
- `AdmissionBundle`
- `AdmissionContract`
- `Request`
- `ActionDescriptor`
- `Permit`

### Admission-blocking objects
- `Manifest`
- `ManifestEntry`
- `BundleContentBinding`
- `VerificationResult`
- `VerificationClaim`
- `RequestShape`
- `RequestBounds`
- `AdmissionCondition`
- `WitnessBinding`
- `ActionBinding`
- `ReplayBinding`

### Support-structuring objects
- `CanonicalIdentityRecord`
- `RefusalCode`
- `RefusalClass`
- `PermitBinding`

---

## 7. Object-level fail-closed triggers

Admission-blocking fail-closed triggers include:
- unrecognized principal family where recognized one is required
- family ambiguity in an authority-bearing role
- incomplete mandatory semantics
- unstable or conflicting identity
- missing required binding
- binding mismatch
- self-contradiction
- conflict with primitive identity
- conflict with manifest law
- conflict with contract closure
- replay-relevant incompleteness where required
- output object not lawfully bound to source decision context

Any such trigger, when admission-relevant, must project to refusal.

---

## 8. Structural versus semantic validity

Structural validity concerns parseability and formal shape.
Semantic validity concerns role, completeness, identity, and lawful binding.

Structural validity alone is never sufficient for positive authority.

---

## 9. Conformance criterion

An implementation conforms to this object model only if:
1. every normative admission-relevant object maps to one defined family
2. identity-bearing objects have stable canonical identities
3. authority-bearing objects are semantically complete
4. required bindings are explicit or recoverable under fixed law
5. family ambiguity is not used as authority
6. manifest/bundle/request/permit/refusal relations are preserved
7. outputs remain structured and typed
8. replay relation is preserved where required
9. no hidden extra family silently carries positive authority

---

## 10. Final object-model law statement

BCF Primitive One operates over a closed normative object universe in which each authority-bearing or admission-relevant object belongs to an explicit principal family, carries fixed role semantics, has stable canonical identity where identity matters, and is valid only when structurally sound, semantically complete, and lawfully bound to the other normative objects required for its role; no object outside this universe, no ambiguous object, no incompletely bound object, and no implicitly interpreted object may lawfully contribute positive admission authority, while any admission-relevant invalidity, incompleteness, ambiguity, identity failure, or binding failure must operate fail-closed and thereby block lawful `ALLOW`.

That is the object model.
