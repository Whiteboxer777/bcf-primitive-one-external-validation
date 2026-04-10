# `SPEC/ADEQUACY_MATRIX.md`

## 0. Status

This document is the normative adequacy-matrix specification for **BCF Primitive One**.

Its function is to define, in exact law-to-machine form, how the ordered `SPEC/` family is saturated by executable surfaces, corpus surfaces, expected observables, audit evidence, and parity/equivalence evidence in the current canonical main line.

This document is not a high-level status note.
It is not a vague roadmap.
It is not a claim of perfection by assertion.

It is the **explicit adequacy ledger** of the current primitive line.

This document must be read together with the full `SPEC/` family, especially:

- `SPEC/INDEX.md`
- `SPEC/PRIMITIVE_LAW.md`
- `SPEC/ADMISSION_SEMANTICS.md`
- `SPEC/CANONICALIZATION_LAW.md`
- `SPEC/VERIFICATION_LAW.md`
- `SPEC/REFUSAL_ALGEBRA.md`
- `SPEC/PERMIT_ALGEBRA.md`
- `SPEC/PRIMITIVE_EQUIVALENCE.md`
- `SPEC/THEOREM_SET.md`

Where a row below refers to a concrete executable or corpus surface, the path names are normative traceability anchors for the current release line.

---

# 1. Closed status vocabulary

Every adequacy row uses exactly one status from the following closed set.

## `FULL`
The law claim is explicitly specified, concretely realized, corpus-witnessed, audit-visible, and parity-relevant where applicable.

## `PARTIAL`
The law claim is explicitly specified and materially realized, but at least one closure dimension remains incomplete, narrow, or only same-family witnessed.

## `LAW_ONLY`
The law claim is explicit but not yet sufficiently realized or evidenced at executable boundary level.

## `MISSING`
The law line requires the claim, but the current release line has no adequate traceable realization.

## `OUT_OF_SCOPE`
The item is outside the lawful primitive scope and therefore not a primitive adequacy obligation.

---

# 2. Canonical matrix columns

Every row below uses the following exact columns.

- `LAW_UNIT_ID`
- `LAW_SOURCE`
- `LAW_CLAIM`
- `EXEC_SURFACE`
- `CORPUS_SURFACE`
- `EXPECTED_OBSERVABLE`
- `AUDIT_EVIDENCE`
- `ADEQUACY_STATUS`
- `GAP_NOTES`

---

# 3. Top-line adequacy summary

| Family | Current line status | Exact meaning |
|---|---|---|
| Spec-family anchoring | FULL | `SPEC/` is the controlling law source inside the main zip and is cross-referenced from release docs. |
| Verification surface | FULL | Verifier, standalone verifier, schema validation, theorem-family corpus, and adversarial bundle-mutation harnesses all exist and are wired. |
| Admission surface | FULL | Runtime evaluator, replay surface, theorem-family corpus, and adversarial request/action corpus all exist and are wired. |
| Refusal surface | FULL | Runtime, verifier, replay, independent implementation, schema harness, and adversarial precedence cases all land in the same refusal object family. |
| Permit surface | FULL | Runtime and independent runtime emit structured permits with explicit binding and authority; schema harness and boundedness probes exist. |
| Canonicalization surface | FULL | Request, action, and generic-object equality/distinctness/idempotence witnesses now exist with dedicated saturation gate and report artifacts. |
| No-bypass surface | FULL | Dedicated refusal path, theorem-family family, and adversarial direct-entrypoint probes exist. |
| Theorem-family dedicated corpora | FULL | Every theorem family has a dedicated family directory and executable harness coverage. |
| Independent second implementation parity | PARTIAL | Primary vs independent second implementation parity exists for verification/runtime/replay and adversarial cases, but still lives in one repository and one language family. |
| Theorem-family row-by-row saturation | FULL | The current matrix now contains explicit row-by-row traceability for the theorem families and critical law clusters. |
| Executable adequacy contract | FULL | The matrix is now mirrored into machine-readable contract form and gated by an explicit adequacy-matrix gate. |
| Externalized second-line contract | FULL | Node repo export, export-prepared cross-repo parity gate, and theorem-discharge coupling are explicitly represented as adequacy rows. |
| Compiled backend preparation | FULL | Kernel-scoped compiled backend artifact, schema, compiler emission, verifier recomputation, and parity gate exist and are truth-bounded. |
| Witness certificate preparation | FULL | Verification, permit, and refusal outputs carry schema-closed witness certificates; canonical bundles emit sample witness-certificate artifacts; dedicated witness-certificate gate exists and is truth-bounded. |

---

# 4. Spec-family anchoring rows

| LAW_UNIT_ID | LAW_SOURCE | LAW_CLAIM | EXEC_SURFACE | CORPUS_SURFACE | EXPECTED_OBSERVABLE | AUDIT_EVIDENCE | ADEQUACY_STATUS | GAP_NOTES |
|---|---|---|---|---|---|---|---|---|
| IDX-01 | `SPEC/INDEX.md` | `SPEC/` is the single normative source family inside the main zip. | release tree + root docs + `SPEC/INDEX.md` | release structure inspection | one `SPEC/` family, no competing law source | zip tree, `README.md`, `CLAIM.md`, `SPEC/INDEX.md` | FULL | None. |
| IDX-02 | `SPEC/INDEX.md` | law-over-code discipline is explicit. | `SPEC/INDEX.md`, `LAW_ALIGNMENT_REPORT.md`, release docs | release structure inspection | spec cited as controlling source | `SPEC/INDEX.md`, `LAW_ALIGNMENT_REPORT.md` | FULL | None. |
| IDX-03 | `SPEC/INDEX.md` | non-spec docs are subordinate to `SPEC/`. | root docs | release structure inspection | root docs point to `SPEC/INDEX.md` and do not redefine law | `README.md`, `CLAIM.md`, `LIMITS.md`, `REPRODUCE.md` | FULL | None. |

---

# 5. Primitive-law rows

| LAW_UNIT_ID | LAW_SOURCE | LAW_CLAIM | EXEC_SURFACE | CORPUS_SURFACE | EXPECTED_OBSERVABLE | AUDIT_EVIDENCE | ADEQUACY_STATUS | GAP_NOTES |
|---|---|---|---|---|---|---|---|---|
| PL-01 | `SPEC/PRIMITIVE_LAW.md` | final verdict universe is exactly `{ALLOW, REFUSAL}` | `src/bcf_primitive/runtime.py`, `src/bcf_primitive_verifier/runtime.py`, `src/bcf_primitive_independent/runtime.py` | `corpus/theorem_families/admission/*`, `corpus/theorem_families/fail_closed/*`, `corpus/adversarial/admission/*` | runtime/replay outputs only `ALLOW` or refusal-object `REFUSAL` | `dist/theorem_family_corpus_report.json`, `dist/adversarial_closure_report.json` | FULL | None. |
| PL-02 | `SPEC/PRIMITIVE_LAW.md` | official positive path requires verified bundle -> admission -> permit | compiler + verifier + runner surfaces | theorem-family `verification`, `admission`, `permit`, `no_bypass` | allow only after verification and permit construction | `dist/equivalence_report.json`, `dist/theorem_family_corpus_report.json` | FULL | None. |
| PL-03 | `SPEC/PRIMITIVE_LAW.md` | final negative landing is structured refusal | verifier runtime + replay + independent implementation + refusal constructor | theorem-family `refusal`, `fail_closed`; adversarial `verification`, `admission`, `refusal_precedence` | blocker cases end as refusal objects, not raw errors | `dist/schema_validation_report.json`, `dist/adversarial_closure_report.json` | FULL | None. |
| PL-04 | `SPEC/PRIMITIVE_LAW.md` | fail-closed behavior holds for admission-relevant failures | runtime refusal path + verifier refusal path + replay refusal path | theorem-family `fail_closed`; adversarial `verification`, `admission` | blocker -> refusal, never allow | `dist/theorem_family_corpus_report.json`, `dist/adversarial_closure_report.json` | FULL | None. |
| PL-05 | `SPEC/PRIMITIVE_LAW.md` | no lawful positive bypass exists outside official path | `refuse_non_bypass`, runner-only release path | theorem-family `no_bypass`, adversarial `no_bypass` | direct bypass probe -> `REFUSE_NON_BYPASS_VIOLATION` | `dist/theorem_family_corpus_report.json`, `dist/adversarial_closure_report.json` | FULL | None. |

---

# 6. Verification-law saturation rows

| LAW_UNIT_ID | LAW_SOURCE | LAW_CLAIM | EXEC_SURFACE | CORPUS_SURFACE | EXPECTED_OBSERVABLE | AUDIT_EVIDENCE | ADEQUACY_STATUS | GAP_NOTES |
|---|---|---|---|---|---|---|---|---|
| VF-01 | `SPEC/VERIFICATION_LAW.md` | verification result space is exactly `{VERIFIED, NOT_VERIFIED}` at verification boundary | `src/bcf_primitive_verifier/verifier.py`, `src/bcf_primitive_independent/verifier.py` | theorem-family `verification`; adversarial `verification` | verified bundle -> `VERIFIED`; mutated bundles -> refusal/`NOT_VERIFIED` | `dist/schema_validation_report.json`, `dist/independent_second_implementation_parity_report.json` | FULL | None. |
| VF-02 | `SPEC/VERIFICATION_LAW.md` | primitive applicability is required for lawful verification | verifier contract + schema/title checks + primitive identity constants | theorem-family `primitive_identity`, `verification` | outputs carry `primitive_identity = BCF Primitive One` | `dist/theorem_family_corpus_report.json` | FULL | None. |
| VF-03 | `SPEC/VERIFICATION_LAW.md` | required bundle files are mandatory | `_verify_required_files`, `_required_files` | theorem-family `verification`; adversarial `VF-A1`, `VF-A8` | missing `TRUST_ROOTS.json` -> `REFUSE_REQUIRED_FILES_MISSING` | `dist/adversarial_closure_report.json` | FULL | None. |
| VF-04 | `SPEC/VERIFICATION_LAW.md` | forbidden undeclared top-level content is blocking | `_verify_no_forbidden_top_level`, `_top_level` | theorem-family `verification`; adversarial `VF-A2`, `VF-A8` | illegal extra file -> `REFUSE_UNDECLARED_FILE` | `dist/adversarial_closure_report.json` | FULL | None. |
| VF-05 | `SPEC/VERIFICATION_LAW.md` | contract mismatch blocks verification | `_verify_contract`, independent `_contract` | theorem-family `verification`; adversarial `VF-A3`, `RA-A2` | tampered contract -> `REFUSE_CONTRACT_MISMATCH` | `dist/adversarial_closure_report.json` | FULL | None. |
| VF-06 | `SPEC/VERIFICATION_LAW.md` | manifest mismatch blocks verification | `_verify_manifest`, independent `_manifest` | theorem-family `verification`; adversarial `VF-A4` | tampered manifest -> `REFUSE_MANIFEST_MISMATCH` | `dist/adversarial_closure_report.json` | FULL | None. |
| VF-07 | `SPEC/VERIFICATION_LAW.md` | compiler product mismatch blocks verification | `_verify_compiler_products`, `tools/verification_subfamily_completion_harness.py` | theorem-family `verification`; adversarial `verification_subfamilies/compiler_product_mismatch` | broken compiler product family -> `REFUSE_COMPILER_PRODUCT_MISMATCH` with schema-valid refusal parity across primary, independent, and externalized lines | `dist/verification_subfamily_completion_report.json`, `dist/node_verification_subfamily_parity_report.json` | FULL | None. |
| VF-08 | `SPEC/VERIFICATION_LAW.md` | certificate invalidity blocks verification | `_verify_certificates`, `tools/verification_subfamily_completion_harness.py` | theorem-family `verification`; adversarial `verification_subfamilies/certificate_invalidity` | certificate invalidity -> `REFUSE_CERTIFICATE_INVALID` with schema-valid refusal parity across primary, independent, and externalized lines | `dist/verification_subfamily_completion_report.json`, `dist/node_verification_subfamily_parity_report.json` | FULL | None. |
| VF-09 | `SPEC/VERIFICATION_LAW.md` | governance invalidity blocks verification | `_verify_governance`, `tools/verification_subfamily_completion_harness.py` | theorem-family `verification`; adversarial `verification_subfamilies/governance_invalidity` | governance invalidity -> `REFUSE_GOVERNANCE_INVALID` with schema-valid refusal parity across primary, independent, and externalized lines | `dist/verification_subfamily_completion_report.json`, `dist/node_verification_subfamily_parity_report.json` | FULL | None. |
| VF-10 | `SPEC/VERIFICATION_LAW.md` | verdict schema validity is explicit and blocking | `_verify_verdict_schema`, independent `_schema_file`, `tools/verification_subfamily_completion_harness.py` | theorem-family `verification`; adversarial `verification_subfamilies/verdict_schema_tamper` | verdict schema tamper -> `REFUSE_VERDICT_SCHEMA_INVALID` with schema-valid refusal parity across primary, independent, and externalized lines | `dist/verification_subfamily_completion_report.json`, `dist/node_verification_subfamily_parity_report.json` | FULL | None. |
| VF-11 | `SPEC/VERIFICATION_LAW.md` | verification schema validity is explicit and blocking | `_verify_verification_schema`, independent `_schema_file` | theorem-family `verification`; adversarial `VF-A5` | invalid verification schema -> `REFUSE_VERIFICATION_SCHEMA_INVALID` | `dist/adversarial_closure_report.json` | FULL | None. |
| VF-12 | `SPEC/VERIFICATION_LAW.md` | refusal schema validity is explicit and blocking | `_verify_refusal_schema`, independent `_schema_file`, `tools/verification_subfamily_completion_harness.py` | theorem-family `verification`; adversarial `verification_subfamilies/refusal_schema_tamper` | refusal schema tamper -> `REFUSE_REFUSAL_SCHEMA_INVALID` with schema-valid refusal parity across primary, independent, and externalized lines | `dist/verification_subfamily_completion_report.json`, `dist/node_verification_subfamily_parity_report.json` | FULL | None. |
| VF-13 | `SPEC/VERIFICATION_LAW.md` | permit schema validity is explicit and blocking | `_verify_permit_schema`, independent `_schema_file`, `tools/verification_subfamily_completion_harness.py` | theorem-family `verification`; schema harness; adversarial `verification_subfamilies/permit_schema_tamper` | permit schema tamper -> `REFUSE_PERMIT_SCHEMA_INVALID` with schema-valid refusal parity across primary, independent, and externalized lines | `dist/schema_validation_report.json`, `dist/verification_subfamily_completion_report.json` | FULL | None. |
| VF-14 | `SPEC/VERIFICATION_LAW.md` | claim/TCB consistency is explicit and blocking | `_verify_claim_and_tcb`, independent `_claim_and_tcb`, `tools/verification_subfamily_completion_harness.py` | theorem-family `verification`; adversarial `verification_subfamilies/claim_tcb_tamper` | claim/TCB tamper -> `REFUSE_CLAIM_TCB_INVALID` with schema-valid refusal parity across primary, independent, and externalized lines | `dist/verification_subfamily_completion_report.json`, `dist/node_verification_subfamily_parity_report.json` | FULL | None. |
| VF-15 | `SPEC/VERIFICATION_LAW.md` | claim matrix consistency is explicit and blocking | `_verify_claim_matrix`, independent `_claim_matrix` | theorem-family `verification`; adversarial `VF-A6` | empty/broken claim matrix -> `REFUSE_CLAIM_MATRIX_INVALID` | `dist/adversarial_closure_report.json` | FULL | None. |
| VF-16 | `SPEC/VERIFICATION_LAW.md` | witness replay consistency is explicit and blocking | `_verify_witnesses`, independent `_witness_replay` | theorem-family `verification`; adversarial `VF-A7` | broken witness replay -> `REFUSE_WITNESS_REPLAY_FAILED` | `dist/adversarial_closure_report.json` | FULL | None. |
| VF-17 | `SPEC/VERIFICATION_LAW.md` | lawful allow is impossible without verified boundary | runner init + replay runtime + theorem harnesses | theorem-family `impossibility`, `verification`; adversarial verification family | any `NOT_VERIFIED` bundle blocks allow in runtime and replay | `dist/theorem_family_corpus_report.json`, `dist/adversarial_closure_report.json` | FULL | None. |

---

# 7. Admission-semantics saturation rows

| LAW_UNIT_ID | LAW_SOURCE | LAW_CLAIM | EXEC_SURFACE | CORPUS_SURFACE | EXPECTED_OBSERVABLE | AUDIT_EVIDENCE | ADEQUACY_STATUS | GAP_NOTES |
|---|---|---|---|---|---|---|---|---|
| AS-01 | `SPEC/ADMISSION_SEMANTICS.md` | lawful allow requires verified bundle plus request success | `SealedBoundaryRunner.execute`, `replay_verdict`, independent runtime/replay | theorem-family `admission`, `impossibility`; adversarial `admission` | allow case -> `ALLOW`, not-verified bundle -> refusal | `dist/theorem_family_corpus_report.json`, `dist/adversarial_closure_report.json` | FULL | None. |
| AS-02 | `SPEC/ADMISSION_SEMANTICS.md` | request must be structurally valid | runtime request validation + independent `_validate_request` | theorem-family `fail_closed`; adversarial `AD-A4` | string request -> `REFUSE_SCHEMA_INVALID` | `dist/adversarial_closure_report.json` | FULL | None. |
| AS-03 | `SPEC/ADMISSION_SEMANTICS.md` | request bounds are enforced fail-closed | runtime byte-size guard + independent size guard | theorem-family `fail_closed`; adversarial `AD-A5` | oversize request -> `REFUSE_REQUEST_OVERSIZE` | `dist/adversarial_closure_report.json` | FULL | None. |
| AS-04 | `SPEC/ADMISSION_SEMANTICS.md` | contract non-satisfaction yields refusal | kernel evaluator + runtime refusal path + independent evaluator | theorem-family `admission`; adversarial `AD-A2`, `AD-A3` | amount/vendor failure -> `REFUSE_VERDICT_NOT_ALLOW` | `dist/adversarial_closure_report.json` | FULL | None. |
| AS-05 | `SPEC/ADMISSION_SEMANTICS.md` | action binding is required for lawful permit release | runtime action descriptor validation + independent runtime action validation | theorem-family `permit`; adversarial `AD-A6` | malformed action descriptor -> `REFUSE_ACTION_DESCRIPTOR_INVALID` | `dist/adversarial_closure_report.json` | FULL | None. |
| AS-06 | `SPEC/ADMISSION_SEMANTICS.md` | ambiguity and missing structure land fail-closed rather than permissive | runtime validators + refusal constructor | theorem-family `fail_closed` | invalid request families never become allow | theorem-family report | FULL | None. |
| AS-07 | `SPEC/ADMISSION_SEMANTICS.md` | anti-silence principle: absence of error is not enough; all predicates must hold | combined verifier/runtime path | theorem-family `admission`, `impossibility` | only allow request satisfying profile gets permit | theorem-family report | FULL | None. |

---

# 8. Refusal-algebra saturation rows

| LAW_UNIT_ID | LAW_SOURCE | LAW_CLAIM | EXEC_SURFACE | CORPUS_SURFACE | EXPECTED_OBSERVABLE | AUDIT_EVIDENCE | ADEQUACY_STATUS | GAP_NOTES |
|---|---|---|---|---|---|---|---|---|
| RA-01 | `SPEC/REFUSAL_ALGEBRA.md` | every blocker lands in structured refusal object family | `make_refusal`, runtime negative path, verifier negative path, replay negative path, independent negative path | theorem-family `refusal`, `fail_closed`; adversarial `verification`, `admission`, `refusal_precedence`, `no_bypass` | blocker -> object with primitive identity, refusal code/class, replay binding | `dist/schema_validation_report.json`, `dist/adversarial_closure_report.json` | FULL | None. |
| RA-02 | `SPEC/REFUSAL_ALGEBRA.md` | refusal class/code universe is closed and explicit | `REFUSAL_TAXONOMY`, `CODE_TO_CLASS`, schemas | theorem-family `refusal` | every emitted refusal code belongs to declared class universe | source + schema + theorem-family report | FULL | None. |
| RA-03 | `SPEC/REFUSAL_ALGEBRA.md` | verifier negatives and runtime negatives share one family | verifier/refusal modules re-export and use same taxonomy | theorem-family `refusal`; schema validation harness | primary negative surfaces validate against same schema | `dist/schema_validation_report.json` | FULL | None. |
| RA-04 | `SPEC/REFUSAL_ALGEBRA.md` | replay negatives also normalize into refusal family | `src/bcf_primitive_verifier/runtime.py`, independent replay runtime | theorem-family `refusal`, `impossibility` | replay deny / replay bundle-failure -> refusal object | theorem-family report | FULL | None. |
| RA-05 | `SPEC/REFUSAL_ALGEBRA.md` | multi-failure primary refusal is deterministic | verifier precedence `_PRECEDENCE`, `REFUSAL_CODE_MAP`; independent `_PRECEDENCE`, `_CODE_MAP` | theorem-family `refusal`; adversarial `RA-A1`, `RA-A2` | same multi-failure -> same primary refusal code/class | `dist/adversarial_closure_report.json` | FULL | None. |
| RA-06 | `SPEC/REFUSAL_ALGEBRA.md` | refusal outputs are schema-valid | refusal schema + schema harness | theorem-family `refusal`; schema harness | refusal objects validate against `refusal.schema.json` | `dist/schema_validation_report.json` | FULL | None. |
| RA-07 | `SPEC/REFUSAL_ALGEBRA.md` | refusal outputs remain replay-attributable | refusal `replay_binding` | theorem-family `determinism_replay`, `refusal` | refusal includes bundle/request binding where relevant | theorem-family report | FULL | None. |

---

# 9. Permit-algebra saturation rows

| LAW_UNIT_ID | LAW_SOURCE | LAW_CLAIM | EXEC_SURFACE | CORPUS_SURFACE | EXPECTED_OBSERVABLE | AUDIT_EVIDENCE | ADEQUACY_STATUS | GAP_NOTES |
|---|---|---|---|---|---|---|---|---|
| PA-01 | `SPEC/PERMIT_ALGEBRA.md` | lawful allow yields structured permit object | runtime positive path + independent runtime positive path | theorem-family `permit`; adversarial `admission`, `permit_boundedness` | allow -> permit object, not raw boolean | `dist/schema_validation_report.json`, `dist/adversarial_closure_report.json` | FULL | None. |
| PA-02 | `SPEC/PERMIT_ALGEBRA.md` | permit carries exact binding to primitive/bundle/request/action | `permit_binding` construction in runtime and independent runtime | theorem-family `permit` | permit binding contains primitive/bundle/request/action digests | theorem-family report + schema validation report | FULL | None. |
| PA-03 | `SPEC/PERMIT_ALGEBRA.md` | positive authority is determinate and bounded | `action_authority.kind = release_bound_action_descriptor` | theorem-family `scope`, `permit`; adversarial `PA-A1`, `PA-A2` | authority kind exact and unchanged across implementations | `dist/adversarial_closure_report.json` | FULL | None. |
| PA-04 | `SPEC/PERMIT_ALGEBRA.md` | permit scope does not widen silently | permit boundedness probes | adversarial `PA-A3` | forbidden extra authority keys absent | `dist/adversarial_closure_report.json` | FULL | None. |
| PA-05 | `SPEC/PERMIT_ALGEBRA.md` | permit outputs are schema-valid | permit schema + schema harness | theorem-family `permit`; schema harness | allow permits validate against `permit.schema.json` | `dist/schema_validation_report.json` | FULL | None. |
| PA-06 | `SPEC/PERMIT_ALGEBRA.md` | no permit on refusal path | runtime/replay negative paths | theorem-family `impossibility` | deny path has `permit = False`; no positive authority emitted | theorem-family report | FULL | None. |

---

# 10. Canonicalization-law saturation rows

| LAW_UNIT_ID | LAW_SOURCE | LAW_CLAIM | EXEC_SURFACE | CORPUS_SURFACE | EXPECTED_OBSERVABLE | AUDIT_EVIDENCE | ADEQUACY_STATUS | GAP_NOTES |
|---|---|---|---|---|---|---|---|---|
| C14N-01 | `SPEC/CANONICALIZATION_LAW.md` | semantically equal request forms collapse to same canonical bytes | `canonical_bytes`, `digest_data` | theorem-family `canonicalization`; adversarial `C14N-A1` | equal forms -> equal bytes + equal digest | theorem-family report + adversarial report | FULL | None. |
| C14N-02 | `SPEC/CANONICALIZATION_LAW.md` | materially different request forms do not collapse improperly | `canonical_bytes`, `digest_data` | theorem-family `canonicalization`; adversarial `C14N-A2` | distinct form -> distinct bytes/digest | theorem-family report + adversarial report | FULL | None. |
| C14N-03 | `SPEC/CANONICALIZATION_LAW.md` | canonicalization is idempotent in normative effect for current request surface | `canonical_bytes` | adversarial `C14N-A3` | repeated canonicalization stable | `dist/adversarial_closure_report.json` | FULL | None. |
| C14N-04 | `SPEC/CANONICALIZATION_LAW.md` | bundle/request digests are replay-stable | digest functions + replay harnesses | theorem-family `determinism_replay`; equivalence harness | same request -> same request digest across parity surfaces | `dist/equivalence_report.json`, `dist/theorem_family_corpus_report.json` | FULL | None. |
| C14N-05 | `SPEC/CANONICALIZATION_LAW.md` | admission-relevant canonicalization failure blocks allow where verification requires canonical identity | verifier manifest/content-binding checks | theorem-family `verification`; adversarial manifest tamper cases | identity mismatch -> `NOT_VERIFIED`/refusal | adversarial report | FULL | None. |
| C14N-06 | `SPEC/CANONICALIZATION_LAW.md` | canonicalization family is now saturated for the currently implemented request, action, and generic-object surfaces | `canonical_bytes`, `digest_data`, `tools/object_canonicalization_impossibility_saturation_gate.py` | theorem-family `canonicalization`, adversarial `canonicalization`, adversarial `canonicalization_object_families` | request/action/object equality, distinctness, and idempotence checks all remain green | `dist/theorem_family_corpus_report.json`, `dist/adversarial_closure_report.json`, `dist/object_canonicalization_impossibility_saturation_report.json` | FULL | Saturation is scoped to the currently implemented canonicalization surfaces; not every hypothetical future object-family extension. |

---

# 11. No-bypass saturation rows

| LAW_UNIT_ID | LAW_SOURCE | LAW_CLAIM | EXEC_SURFACE | CORPUS_SURFACE | EXPECTED_OBSERVABLE | AUDIT_EVIDENCE | ADEQUACY_STATUS | GAP_NOTES |
|---|---|---|---|---|---|---|---|---|
| NB-01 | `SPEC/PRIMITIVE_LAW.md`, `SPEC/SCOPE_AND_NON_SCOPE.md` | direct non-official entrypoints land in explicit refusal | `refuse_non_bypass` | theorem-family `no_bypass`; adversarial `NB-A1`, `NB-A2` | refusal code `REFUSE_NON_BYPASS_VIOLATION` | theorem-family + adversarial reports | FULL | None. |
| NB-02 | `SPEC/PERMIT_ALGEBRA.md` | no lawful release without permit realization on official path | runtime only emits `released_action` inside permit object | theorem-family `permit`, `no_bypass` | no detached release object outside permit surface | theorem-family report | FULL | None. |

---

# 12. Theorem-family dedicated corpus saturation rows

| LAW_UNIT_ID | LAW_SOURCE | LAW_CLAIM | EXEC_SURFACE | CORPUS_SURFACE | EXPECTED_OBSERVABLE | AUDIT_EVIDENCE | ADEQUACY_STATUS | GAP_NOTES |
|---|---|---|---|---|---|---|---|---|
| THF-01 | `SPEC/THEOREM_SET.md` | primitive identity theorem family has dedicated executable corpus | `tools/theorem_family_corpus_harness.py` | `corpus/theorem_families/primitive_identity/*` | same primitive identity across verification/permit/refusal | `dist/theorem_family_corpus_report.json` | FULL | None. |
| THF-02 | `SPEC/THEOREM_SET.md` | scope theorem family has dedicated executable corpus | theorem-family harness | `corpus/theorem_families/scope/*` | bounded permit + boundary-fitness verification | theorem-family report | FULL | None. |
| THF-03 | `SPEC/THEOREM_SET.md` | object-model theorem family has dedicated executable corpus | theorem-family harness | `corpus/theorem_families/object_model/*` | verification/permit/refusal structural families present | theorem-family report | FULL | None. |
| THF-04 | `SPEC/THEOREM_SET.md` | canonicalization theorem family has dedicated executable corpus | theorem-family harness + adversarial harness | `corpus/theorem_families/canonicalization/*`, `corpus/adversarial/canonicalization/*` | collapse/idempotence/anti-collapse checks | theorem-family + adversarial reports | FULL | None. |
| THF-05 | `SPEC/THEOREM_SET.md` | verification theorem family has dedicated executable corpus | theorem-family harness + adversarial harness | `corpus/theorem_families/verification/*`, `corpus/adversarial/verification/*` | verification law cluster exercised | theorem-family + adversarial reports | FULL | None. |
| THF-06 | `SPEC/THEOREM_SET.md` | admission theorem family has dedicated executable corpus | theorem-family harness + adversarial harness | `corpus/theorem_families/admission/*`, `corpus/adversarial/admission/*` | allow/refusal biconditional witness cases | theorem-family + adversarial reports | FULL | None. |
| THF-07 | `SPEC/THEOREM_SET.md` | refusal theorem family has dedicated executable corpus | theorem-family harness + adversarial precedence harness | `corpus/theorem_families/refusal/*`, `corpus/adversarial/refusal_precedence/*` | primary refusal determinism + normalized family | theorem-family + adversarial reports | FULL | None. |
| THF-08 | `SPEC/THEOREM_SET.md` | permit theorem family has dedicated executable corpus | theorem-family harness + adversarial boundedness harness | `corpus/theorem_families/permit/*`, `corpus/adversarial/permit_boundedness/*` | permit binding + bounded authority | theorem-family + adversarial reports | FULL | None. |
| THF-09 | `SPEC/THEOREM_SET.md` | determinism/replay theorem family has dedicated executable corpus | theorem-family harness + equivalence harness | `corpus/theorem_families/determinism_replay/*` | replay parity stable | theorem-family + equivalence reports | FULL | None. |
| THF-10 | `SPEC/THEOREM_SET.md` | fail-closed theorem family has dedicated executable corpus | theorem-family harness + adversarial harness | `corpus/theorem_families/fail_closed/*` | blockers land in refusal | theorem-family + adversarial reports | FULL | None. |
| THF-11 | `SPEC/THEOREM_SET.md` | no-bypass theorem family has dedicated executable corpus | theorem-family harness + adversarial harness | `corpus/theorem_families/no_bypass/*`, `corpus/adversarial/no_bypass/*` | no bypass refusal | theorem-family + adversarial reports | FULL | None. |
| THF-12 | `SPEC/THEOREM_SET.md` | equivalence theorem family has dedicated executable corpus | theorem-family harness + independent parity + adversarial equivalence | `corpus/theorem_families/equivalence/*`, `corpus/adversarial/equivalence/*` | primary/independent parity on positive, negative, and mutated-bundle cases | theorem-family + independent parity + adversarial reports | FULL | None. |
| THF-13 | `SPEC/THEOREM_SET.md` | impossibility theorem family has dedicated executable corpus | theorem-family harness | `corpus/theorem_families/impossibility/*` | no allow without verification; no permit on deny | theorem-family report | FULL | None. |
| THF-14 | `SPEC/THEOREM_SET.md` | closure theorem family has dedicated executable corpus | theorem-family harness + release structure check | `corpus/theorem_families/closure/*` | all theorem family dirs and required modules present | theorem-family report | FULL | None. |

---

# 13. Independent second implementation parity rows

| LAW_UNIT_ID | LAW_SOURCE | LAW_CLAIM | EXEC_SURFACE | CORPUS_SURFACE | EXPECTED_OBSERVABLE | AUDIT_EVIDENCE | ADEQUACY_STATUS | GAP_NOTES |
|---|---|---|---|---|---|---|---|---|
| EQ-01 | `SPEC/PRIMITIVE_EQUIVALENCE.md` | independent second implementation preserves verification meaning on canonical valid bundle | `tools/independent_second_implementation_parity.py` + independent verifier | `corpus/equivalence/*` | primary and independent verification parity | `dist/independent_second_implementation_parity_report.json` | FULL | None. |
| EQ-02 | `SPEC/PRIMITIVE_EQUIVALENCE.md` | independent second implementation preserves runtime allow meaning | same as above | `corpus/equivalence/allow_request.json` | both surfaces emit compatible allow/permit meaning | independent parity report | FULL | None. |
| EQ-03 | `SPEC/PRIMITIVE_EQUIVALENCE.md` | independent second implementation preserves runtime deny meaning | same as above | `corpus/equivalence/deny_request.json` | both surfaces emit compatible refusal meaning | independent parity report | FULL | None. |
| EQ-04 | `SPEC/PRIMITIVE_EQUIVALENCE.md` | independent second implementation preserves replay allow/deny meaning | same as above | `corpus/equivalence/*` | replay parity stable | independent parity report | FULL | None. |
| EQ-05 | `SPEC/PRIMITIVE_EQUIVALENCE.md` | independent second implementation preserves adversarial verification parity | `tools/adversarial_closure_harness.py` | `corpus/adversarial/equivalence/*`, verification mutation refs | both surfaces emit same not-verified/refusal code on mutated bundles | `dist/adversarial_closure_report.json` | FULL | None. |
| EQ-06 | `SPEC/PRIMITIVE_EQUIVALENCE.md` | independent second implementation preserves adversarial runtime parity | adversarial closure harness | `corpus/adversarial/equivalence/*` | both surfaces emit same allow/refusal meaning on adversarial runtime cases | adversarial report | FULL | None. |
| EQ-07 | `SPEC/PRIMITIVE_EQUIVALENCE.md` | independent parity is genuine second-surface same-repo parity, not yet cross-repository/cross-language parity | independent implementation family | parity corpus and reports | same-repo independent parity exists | source tree + parity reports | PARTIAL | The current second implementation is structurally separate and law-checked, but still resides in the same repository and Python ecosystem rather than a fully external implementation line. |

---

# 14. Theorem-family row-by-row saturation rows

| LAW_UNIT_ID | LAW_SOURCE | LAW_CLAIM | EXEC_SURFACE | CORPUS_SURFACE | EXPECTED_OBSERVABLE | AUDIT_EVIDENCE | ADEQUACY_STATUS | GAP_NOTES |
|---|---|---|---|---|---|---|---|---|
| THM-PI | `SPEC/THEOREM_SET.md` | primitive-identity theorem family is executable and witnessed | theorem-family harness | theorem family `primitive_identity` | same primitive identity across surfaces | theorem-family report | FULL | None. |
| THM-SC | `SPEC/THEOREM_SET.md` | scope theorem family is executable and witnessed | theorem-family harness + permit boundedness probes | theorem family `scope`, adversarial permit boundedness | bounded permit, bounded verification meaning | theorem-family + adversarial reports | FULL | None. |
| THM-OM | `SPEC/THEOREM_SET.md` | object-model theorem family is executable and witnessed | theorem-family harness + schema harness | theorem family `object_model` | structured object keys and bindings present | theorem-family + schema reports | FULL | None. |
| THM-C14N | `SPEC/THEOREM_SET.md` | canonicalization theorem family is executable and witnessed | theorem-family harness + adversarial canonicalization + equivalence harness | theorem family `canonicalization`, adversarial `canonicalization`, canonical corpus | collapse/idempotence/anti-collapse parity | theorem-family + adversarial + equivalence reports | FULL | None. |
| THM-VF | `SPEC/THEOREM_SET.md` | verification theorem family is executable and witnessed | verifier + independent verifier + theorem-family/adversarial harnesses | theorem family `verification`, adversarial `verification` | verified/not-verified behavior explicit | theorem-family + adversarial + schema reports | FULL | None. |
| THM-AD | `SPEC/THEOREM_SET.md` | admission theorem family is executable and witnessed | runtime + replay + theorem/adversarial harnesses | theorem family `admission`, adversarial `admission` | allow/refusal biconditional witness set | theorem-family + adversarial reports | FULL | None. |
| THM-RA | `SPEC/THEOREM_SET.md` | refusal theorem family is executable and witnessed | refusal constructors + theorem/adversarial harnesses | theorem family `refusal`, adversarial `refusal_precedence` | normalized refusal with deterministic primary code | theorem-family + adversarial + schema reports | FULL | None. |
| THM-PA | `SPEC/THEOREM_SET.md` | permit theorem family is executable and witnessed | runtime positive path + permit schema + permit boundedness harness | theorem family `permit`, adversarial `permit_boundedness` | bounded permit with explicit binding | theorem-family + adversarial + schema reports | FULL | None. |
| THM-DR | `SPEC/THEOREM_SET.md` | determinism/replay theorem family is executable and witnessed | replay runtimes + equivalence harness | theorem family `determinism_replay`, equivalence corpus | replay-stable meaning | theorem-family + equivalence reports | FULL | None. |
| THM-FC | `SPEC/THEOREM_SET.md` | fail-closed theorem family is executable and witnessed | verifier/runtime refusal paths + theorem/adversarial harnesses | theorem family `fail_closed`, adversarial `verification`,`admission` | blockers never bypass into allow | theorem-family + adversarial reports | FULL | None. |
| THM-NB | `SPEC/THEOREM_SET.md` | no-bypass theorem family is executable and witnessed | `refuse_non_bypass` + theorem/adversarial harnesses | theorem family `no_bypass`, adversarial `no_bypass` | non-bypass violation explicit | theorem-family + adversarial reports | FULL | None. |
| THM-EQ | `SPEC/THEOREM_SET.md` | equivalence theorem family is executable and witnessed | independent parity + second-surface parity + adversarial parity | theorem family `equivalence`, adversarial `equivalence` | parity across surfaces and independent implementation | equivalence + parity + adversarial reports | FULL | None. |
| THM-IMP | `SPEC/THEOREM_SET.md` | impossibility theorem family is executable and witnessed | theorem-family harness | theorem family `impossibility` | no allow without verification; no permit on deny | theorem-family report | FULL | None. |
| THM-CL | `SPEC/THEOREM_SET.md` | closure theorem family is executable and witnessed | theorem-family harness + release structure check | theorem family `closure` | required modules and theorem dirs exist | theorem-family report | FULL | None. |

---

# 15. Remaining partials and exact residual gaps

The current line is materially stronger than prior passes. Object-model, canonicalization, and impossibility residuals have now been strengthened by a dedicated saturation gate. The remaining exact residual gaps are reduced to the still-open closure boundaries below.

| GAP_ID | Law region | Current status | Exact residual gap |
|---|---|---|---|
| GAP-04 | Mechanized theorem discharge | LAW_ONLY | The theorem-discharge line is executable-witness strong, but not yet theorem-prover/mechanization grade. |






These partials are explicit and bounded. They are not hidden.

---

# 16. Final adequacy statement for the current pass

The current line of BCF Primitive One now has:

- full theorem-family dedicated corpus families
- explicit adversarial closure families for verification, admission, refusal precedence, permit boundedness, canonicalization, no-bypass, and equivalence
- executable theorem-family witness harnesses
- executable adversarial closure harnesses
- independent second implementation parity on canonical and adversarial surfaces
- explicit row-by-row theorem-family adequacy saturation in this matrix

Accordingly, the remaining open region is no longer broad law-to-machine drift.
It is a much narrower residual region of **additional adversarial saturation depth** in specific verification subfamilies and **stronger external independence** of the second implementation line.

That is the current adequacy state.


# 25. Verification-subfamily adversarial completion rows

The following rows are mandatory saturation rows for the verification law and must be treated as concrete executable adequacy units.

- `VF-SUB-01` — compiler product mismatch -> `tools/verification_subfamily_completion_harness.py` -> `corpus/adversarial/verification_subfamilies/compiler_product_mismatch/*` -> expected observable `REFUSE_COMPILER_PRODUCT_MISMATCH` -> status `FULL`
- `VF-SUB-02` — certificate invalidity -> `tools/verification_subfamily_completion_harness.py` -> `corpus/adversarial/verification_subfamilies/certificate_invalidity/*` -> expected observable `REFUSE_CERTIFICATE_INVALID` -> status `FULL`
- `VF-SUB-03` — governance invalidity -> `tools/verification_subfamily_completion_harness.py` -> `corpus/adversarial/verification_subfamilies/governance_invalidity/*` -> expected observable `REFUSE_GOVERNANCE_INVALID` -> status `FULL`
- `VF-SUB-04` — verdict schema tamper -> `tools/verification_subfamily_completion_harness.py` -> `corpus/adversarial/verification_subfamilies/verdict_schema_tamper/*` -> expected observable `REFUSE_VERDICT_SCHEMA_INVALID` -> status `FULL`
- `VF-SUB-05` — verification schema tamper -> `tools/verification_subfamily_completion_harness.py` -> `corpus/adversarial/verification_subfamilies/verification_schema_tamper/*` -> expected observable `REFUSE_VERIFICATION_SCHEMA_INVALID` -> status `FULL`
- `VF-SUB-06` — refusal schema tamper -> `tools/verification_subfamily_completion_harness.py` -> `corpus/adversarial/verification_subfamilies/refusal_schema_tamper/*` -> expected observable `REFUSE_REFUSAL_SCHEMA_INVALID` -> status `FULL`
- `VF-SUB-07` — permit schema tamper -> `tools/verification_subfamily_completion_harness.py` -> `corpus/adversarial/verification_subfamilies/permit_schema_tamper/*` -> expected observable `REFUSE_PERMIT_SCHEMA_INVALID` -> status `FULL`
- `VF-SUB-08` — claim/tcb tamper -> `tools/verification_subfamily_completion_harness.py` -> `corpus/adversarial/verification_subfamilies/claim_tcb_tamper/*` -> expected observable `REFUSE_CLAIM_TCB_INVALID` -> status `FULL`
- `VF-SUB-09` — claim matrix tamper -> `tools/verification_subfamily_completion_harness.py` -> `corpus/adversarial/verification_subfamilies/claim_matrix_tamper/*` -> expected observable `REFUSE_CLAIM_MATRIX_INVALID` -> status `FULL`
- `VF-SUB-10` — witness replay tamper -> `tools/verification_subfamily_completion_harness.py` -> `corpus/adversarial/verification_subfamilies/witness_replay_tamper/*` -> expected observable `REFUSE_WITNESS_REPLAY_FAILED` -> status `FULL`

# 26. Externalized second implementation line rows

The following rows are mandatory for the externalized second implementation line.

- `EQ-EXT-01` — externalized verification parity -> `tools/externalized_second_line_parity.py` -> expected observable parity on `VERIFIED` / `NOT_VERIFIED` structured meaning -> status `FULL`
- `EQ-EXT-02` — externalized runtime allow parity -> `tools/externalized_second_line_parity.py` -> expected observable parity on permit binding and authority kind -> status `FULL`
- `EQ-EXT-03` — externalized runtime refusal parity -> `tools/externalized_second_line_parity.py` -> expected observable parity on refusal class/code -> status `FULL`
- `EQ-EXT-04` — externalized replay allow parity -> `tools/externalized_second_line_parity.py` -> expected observable parity on replay allow meaning -> status `FULL`
- `EQ-EXT-05` — externalized replay refusal parity -> `tools/externalized_second_line_parity.py` -> expected observable parity on replay refusal meaning -> status `FULL`

## 10.12 `SPEC/THEOREM_DISCHARGE_EXECUTABLE_CONTRACT.md`

### Law role
Defines theorem discharge as an executable contract with a machine-readable ledger mirror, a closed status vocabulary, a gate, a policy file, and release-blocking theorem families.

### Mandatory executable witnesses
- `tools/theorem_discharge_gate.py`
- `PROOFS/THEOREM_DISCHARGE_LEDGER.json`
- `SPEC/THEOREM_DISCHARGE_POLICY.json`

### Corpus surface
- theorem-family corpus families
- adversarial closure corpus families
- verification-subfamily adversarial families

### Expected observable
- theorem discharge gate report with `overall_ok = true`
- release-blocking theorem families at `EXECUTABLE_WITNESS_STRONG`

### Minimum adequacy target
`FULL`

## 10.13 `SPEC/CROSS_REPO_PARITY_EXECUTABLE_CONTRACT.md`

### Law role
Defines cross-repo parity as an executable contract over exported repo reports, workflow templates, and machine-readable parity rules.

### Mandatory executable witnesses
- `tools/cross_repo_parity_ci_gate.py`
- `CI/CROSS_REPO_PARITY_CONTRACT.json`
- `repo_exports/node_second_line_repo/.github/workflows/node-second-line-parity-gate.yml`
- `repo_exports/node_second_line_repo/.github/workflows/node-second-line-cross-repo-artifact.yml`

### Corpus surface
- node out-of-family parity corpus
- node verification-subfamily parity corpus
- exported repo self-check fixtures

### Expected observable
- cross-repo parity CI gate report with `overall_ok = true`
- required workflow templates present
- required export reports present and valid

### Minimum adequacy target
`FULL`

# 17. Theorem-discharge executable-contract rows

| LAW_UNIT_ID | LAW_SOURCE | LAW_CLAIM | EXEC_SURFACE | CORPUS_SURFACE | EXPECTED_OBSERVABLE | AUDIT_EVIDENCE | ADEQUACY_STATUS | GAP_NOTES |
|---|---|---|---|---|---|---|---|---|
| TD-02 | `SPEC/THEOREM_DISCHARGE_EXECUTABLE_CONTRACT.md` | theorem discharge must be mirrored into machine-readable JSON and gated by a closed policy with release-blocking theorem families | `tools/theorem_discharge_gate.py`, `PROOFS/THEOREM_DISCHARGE_LEDGER.json`, `SPEC/THEOREM_DISCHARGE_POLICY.json` | `corpus/theorem_families/*`, `corpus/adversarial/*`, `corpus/adversarial/verification_subfamilies/*` | `dist/theorem_discharge_gate_report.json` with `overall_ok = true` | `dist/theorem_discharge_gate_report.json`, `PROOFS/THEOREM_DISCHARGE_LEDGER.json`, `SPEC/THEOREM_DISCHARGE_POLICY.json` | FULL | None. |

# 18. Cross-repo parity executable-contract rows

| LAW_UNIT_ID | LAW_SOURCE | LAW_CLAIM | EXEC_SURFACE | CORPUS_SURFACE | EXPECTED_OBSERVABLE | AUDIT_EVIDENCE | ADEQUACY_STATUS | GAP_NOTES |
|---|---|---|---|---|---|---|---|---|
| EXT-06 | `SPEC/CROSS_REPO_PARITY_EXECUTABLE_CONTRACT.md` | export-prepared cross-repo parity must be machine-gated over exported repo reports and required workflow templates | `tools/cross_repo_parity_ci_gate.py`, `CI/CROSS_REPO_PARITY_CONTRACT.json`, `repo_exports/node_second_line_repo/.github/workflows/node-second-line-parity-gate.yml`, `repo_exports/node_second_line_repo/.github/workflows/node-second-line-cross-repo-artifact.yml` | `corpus/equivalence/*`, `corpus/adversarial/verification_subfamilies/*`, `repo_exports/node_second_line_repo/fixtures/*` | `dist/cross_repo_parity_ci_gate_report.json` with `overall_ok = true` | `dist/cross_repo_parity_ci_gate_report.json`, `CI/CROSS_REPO_PARITY_CONTRACT.json`, `repo_exports/node_second_line_repo/.github/workflows/node-second-line-cross-repo-artifact.yml` | FULL | None. |


## Mechanized-kernel executable-contract rows

| LAW_UNIT_ID | LAW_SOURCE | LAW_CLAIM | EXEC_SURFACE | CORPUS_SURFACE | EXPECTED_OBSERVABLE | AUDIT_EVIDENCE | ADEQUACY_STATUS | GAP_NOTES |
|---|---|---|---|---|---|---|---|---|
| MK-01 | `PROOFS/MECHANIZED_KERNEL_SCOPE.md`, `PROOFS/SEMANTIC_CORE_FORMALIZATION.md`, `SPEC/THEOREM_SET.md` | Mechanized kernel preparation exists for verdict totality, verification necessity, fail-closed core, admission biconditional core, no-bypass core, and canonicalization subset core. | `mechanized_kernel/semantic_core.py`, `mechanized_kernel/checker.py`, `tools/mechanized_kernel_gate.py` | `corpus/canonicalization/*` plus exhaustive finite abstract state space | `overall_ok = true` with 4096-state finite kernel pass and canonicalization subset parity/idempotence checks | `dist/mechanized_kernel_gate_report.json`, `PROOFS/MECHANIZED_KERNEL_SCOPE.md`, `PROOFS/MECHANIZED_THEOREM_MAP.md`, `PROOFS/PROOF_OBLIGATIONS.md`, `PROOFS/SEMANTIC_CORE_FORMALIZATION.md` | FULL | Preparation-scope mechanized kernel only; not whole-family theorem-prover discharge. |


# 16. Admission normal form executable adequacy

| LAW_UNIT_ID | LAW_SOURCE | LAW_CLAIM | EXEC_SURFACE | CORPUS_SURFACE | EXPECTED_OBSERVABLE | AUDIT_EVIDENCE | ADEQUACY_STATUS | GAP_NOTES |
|---|---|---|---|---|---|---|---|---|
| ANF-01 | `SPEC/ADMISSION_NORMAL_FORM.md`; `SPEC/ADMISSION_NORMAL_FORM_EXECUTABLE_CONTRACT.md` | Kernel-scoped normalized admission profiles compile to deterministic DNF literal-clause artifacts that preserve reference verdict meaning on the canonical kernel corpus and are emitted as verifier-checkable compiler products. | `src/bcf_primitive_verifier/admission_normal_form.py`; `src/bcf_primitive/compiler.py`; `src/bcf_primitive_verifier/verifier.py`; `tools/admission_normal_form_gate.py` | `examples/canonical/invoice_profile*.json`, `examples/canonical/invoice_request_allow.json`, `examples/canonical/invoice_deny_request.json` | `dist/admission_normal_form_gate_report.json` has `overall_ok = true`; fresh bundles contain `ADMISSION_NORMAL_FORM.json`; verifier compiler-product check for `admission_normal_form` is `true` | `REPORTS/admission_normal_form_gate_report.json` `dist/admission_normal_form_gate_report.json` | FULL | Kernel-scoped only. This row does not claim whole-family final IR closure or scalable compiled backend correctness. |


# 19. Compiled-backend executable adequacy

| LAW_UNIT_ID | LAW_SOURCE | LAW_CLAIM | EXEC_SURFACE | CORPUS_SURFACE | EXPECTED_OBSERVABLE | AUDIT_EVIDENCE | ADEQUACY_STATUS | GAP_NOTES |
|---|---|---|---|---|---|---|---|---|
| CB-01 | `SPEC/COMPILED_BACKEND.md`, `SPEC/COMPILED_BACKEND_EXECUTABLE_CONTRACT.md` | Kernel-scoped ANF artifacts compile into deterministic indexed compiled-backend artifacts that preserve verdict class on the current kernel corpus and are emitted as verifier-checkable compiler products. | `src/bcf_primitive_verifier/compiled_backend.py`, `src/bcf_primitive/compiler.py`, `src/bcf_primitive_verifier/verifier.py`, `tools/compiled_backend_gate.py` | `examples/canonical/invoice_profile*.json`, `examples/canonical/invoice_request_allow.json`, `examples/canonical/invoice_deny_request.json` | `dist/compiled_backend_gate_report.json` has `overall_ok = true`; fresh bundles contain `COMPILED_BACKEND.json`; verifier compiler-product check for `compiled_backend` is `true` | `REPORTS/compiled_backend_gate_report.json`, `dist/compiled_backend_gate_report.json`, `schemas/compiled_backend.schema.json` | FULL | Preparation-scope only. This row does not claim whole-family compiled-backend correctness or final scalable backend completeness. |


# 20. Witness-certificate executable adequacy

| LAW_UNIT_ID | LAW_SOURCE | LAW_CLAIM | EXEC_SURFACE | CORPUS_SURFACE | EXPECTED_OBSERVABLE | AUDIT_EVIDENCE | ADEQUACY_STATUS | GAP_NOTES |
|---|---|---|---|---|---|---|---|---|
| WC-01 | `SPEC/WITNESS_CERTIFICATES.md`, `SPEC/WITNESS_CERTIFICATES_EXECUTABLE_CONTRACT.md` | Kernel-scoped verification, permit, and refusal outputs carry schema-closed digest-bound witness certificates; canonical bundles emit sample witness-certificate artifacts; verifier and runtime surfaces preserve source-digest fidelity. | `src/bcf_primitive_verifier/witness_certificate.py`, `src/bcf_primitive/runtime.py`, `src/bcf_primitive_verifier/runtime.py`, `src/bcf_primitive_verifier/verifier.py`, `tools/witness_certificate_gate.py` | `examples/canonical/invoice_profile*.json`, compiled sample bundle witness-certificate artifacts, runtime allow/deny and replay refusal outputs | `dist/witness_certificate_gate_report.json` has `overall_ok = true`; runtime and verification outputs contain valid witness certificates; sample bundle witness certificates validate and digest-check | `REPORTS/witness_certificate_gate_report.json`, `dist/witness_certificate_gate_report.json`, `schemas/witness_certificate.schema.json`, `PROOFS/WITNESS_CERTIFICATES_SCOPE.md`, `PROOFS/WITNESS_CERTIFICATES_THEOREM_MAP.md` | FULL | Preparation-scope only. This row does not claim whole-family proof certificates or theorem-prover discharge. |
| WC-02 | `SPEC/WITNESS_CERTIFICATE_EXPANSION.md`, `SPEC/WITNESS_CERTIFICATE_EXPANSION_EXECUTABLE_CONTRACT.md` | Witness certificates carry explicit version/scope/source-kind/binding-digest/claim-set-digest discipline; replay and no-bypass witness artifacts exist; witness parity holds across primary, independent, externalized, and Node runtime/replay/verification surfaces on the current implemented kernel corpus. | `src/bcf_primitive_verifier/witness_certificate.py`, `src/bcf_primitive_independent/runtime.py`, `externalized_second_line/src/bcf_primitive_externalized/runtime.py`, `node_second_line/src/witness_certificate.mjs`, `tools/witness_certificate_expansion_gate.py` | canonical invoice profile + allow/deny requests + runtime/replay/no-bypass paths + expanded sample witness bundle artifacts | `dist/witness_certificate_expansion_report.json` has `overall_ok = true`; expanded sample witness artifacts validate; cross-implementation witness cores remain aligned on current implemented surfaces | `REPORTS/witness_certificate_expansion_report.json`, `dist/witness_certificate_expansion_report.json`, `PROOFS/WITNESS_CERTIFICATE_EXPANSION_SCOPE.md`, `PROOFS/WITNESS_CERTIFICATE_EXPANSION_THEOREM_MAP.md` | FULL | Scoped executable-witness expansion only; not minimal proof certificates or theorem-prover-grade certificate closure. |
| WFME-01 | `SPEC/WHOLE_FAMILY_MECHANIZATION_EXPANSION.md`, `SPEC/WHOLE_FAMILY_MECHANIZATION_EXPANSION_EXECUTABLE_CONTRACT.md`, `SPEC/THEOREM_SET.md` | A scoped executable-witness whole-family mechanization expansion line exists across the mechanized kernel, ANF, compiled backend, witness-certificate carrying outputs, and selected fail-closed / no-bypass boundary paths. | `tools/whole_family_mechanization_expansion_gate.py`, `mechanized_kernel/*`, `src/bcf_primitive_verifier/admission_normal_form.py`, `src/bcf_primitive_verifier/compiled_backend.py`, `src/bcf_primitive_verifier/witness_certificate.py` | canonical invoice profiles + allow/deny requests + runtime/replay/no-bypass paths + broken-bundle verification path | `dist/whole_family_mechanization_expansion_report.json` has `overall_ok = true` and cross-layer preservation checks remain green | `REPORTS/whole_family_mechanization_expansion_report.json`, `dist/whole_family_mechanization_expansion_report.json`, `PROOFS/WHOLE_FAMILY_MECHANIZATION_EXPANSION_SCOPE.md`, `PROOFS/WHOLE_FAMILY_MECHANIZATION_EXPANSION_THEOREM_MAP.md` | FULL | Scoped executable-witness expansion only; not theorem-prover-grade whole-family discharge. |

| OCI-01 | `SPEC/OBJECT_CANONICALIZATION_IMPOSSIBILITY_SATURATION.md`, `SPEC/OBJECT_CANONICALIZATION_IMPOSSIBILITY_SATURATION_EXECUTABLE_CONTRACT.md`, `SPEC/THEOREM_SET.md` | Dedicated executable saturation exists for object-model, canonicalization, and impossibility theorem regions. | `tools/object_canonicalization_impossibility_saturation_gate.py` | theorem-family object_model/canonicalization/impossibility corpora + dedicated adversarial families | `overall_ok = true`; object schemas valid and malformed mutations rejected; request/action/object canonicalization parity holds; impossibility constraints hold | `dist/object_canonicalization_impossibility_saturation_report.json`, `PROOFS/OBJECT_CANONICALIZATION_IMPOSSIBILITY_SATURATION_SCOPE.md`, `PROOFS/OBJECT_CANONICALIZATION_IMPOSSIBILITY_SATURATION_THEOREM_MAP.md` | FULL | Scoped executable-witness saturation only; not theorem-prover-grade whole-family closure. |
