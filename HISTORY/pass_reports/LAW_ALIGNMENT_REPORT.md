# LAW_ALIGNMENT_REPORT.md

## Status

This document is the finalization-oriented concrete law-to-code alignment report for the current BCF Primitive One release line.

It is not controlling law. The controlling law source is:

- `SPEC/INDEX.md`
- and the ordered `SPEC/` family it governs.

This report exists to state, without historical accumulation or release drift, what is currently aligned, what is strongly evidenced, what remains partial, and where the largest remaining closure gaps still are.

---

## 1. Exact scope of this report

This report covers the highest-value alignment surfaces now present in the main release line:

1. verification
2. admission
3. refusal
4. permit
5. canonicalization
6. no-bypass
7. theorem-family corpus closure
8. adversarial closure
9. second-implementation parity
10. theorem-discharge evidence coupling

It supersedes earlier pass-by-pass narrative fragments.

---

## 2. What is concretely integrated in the release line

The current release line now contains, together in one canonical zip:

- one ordered normative `SPEC/` law family
- one concrete `SPEC/ADEQUACY_MATRIX.md`
- one primary Python implementation line
- one verifier line
- one independent Python second implementation line
- one externalized Python second line
- one out-of-family Node.js second line
- theorem-family corpus families
- adversarial corpus families
- verification-subfamily adversarial completion families
- schema-validation harnesses
- equivalence harnesses
- theorem-discharge evidence artifacts

This means the release is no longer only a law pack or only a code pack. It is a law-to-machine release family.

---

## 3. Cluster-by-cluster alignment judgment

### 3.1 Verification

**Current judgment:** strong executable-witness alignment.

**What is concretely aligned:**
- standalone verifier surface exists
- verifier emits explicit `VERIFIED` / refusal-shaped `NOT_VERIFIED` outputs
- manifest and content-binding checks are active
- required-file presence is active
- forbidden undeclared top-level content blocking is active
- verification schema, refusal schema, and permit schema checks are present
- verification-subfamily adversarial completion families are present
- parity exists across:
  - primary verifier
  - independent Python verifier
  - externalized Python verifier
  - Node.js verifier

**Residual limitation:**
- this is strong executable witness and parity closure, not theorem-prover discharge of the verification theorem family
- second-language parity exists in the same release line, not yet as a separately governed repository/toolchain with independent CI

**Release status:** strong and materially valuable.

---

### 3.2 Admission

**Current judgment:** strong executable-witness alignment.

**What is concretely aligned:**
- deterministic allow/refusal reduction exists
- request validation, shape/bounds-style rejection, and contract-based allow/deny behavior are exercised
- oversize and schema-invalid requests land fail-closed
- action descriptor validation is active
- theorem-family and adversarial corpus families exercise positive and negative admission paths
- parity exists across primary, independent, externalized, and Node.js surfaces for core admission cases

**Residual limitation:**
- named semantic predicates still remain primarily law-level concepts; they are strongly witnessed by harnesses and outputs, but not all appear as separately materialized runtime artifacts

**Release status:** strong and materially valuable.

---

### 3.3 Refusal

**Current judgment:** strong executable-witness alignment.

**What is concretely aligned:**
- runtime negatives are refusal-object based
- verifier negatives are normalized into the same refusal family
- replay negatives also land in refusal-object form
- refusal class/code taxonomy is explicit and closed in release artifacts
- multi-failure primary refusal behavior is exercised adversarially
- refusal schema validation exists
- parity exists across Python and Node.js second-line surfaces

**Residual limitation:**
- strong executable witness does not equal theorem-prover-complete proof of refusal completeness

**Release status:** strong and materially valuable.

---

### 3.4 Permit

**Current judgment:** strong executable-witness alignment.

**What is concretely aligned:**
- runtime positive outputs are structured permit objects
- permit binding is explicit
- action authority is explicit and bounded
- permit schema exists and is validated
- permit-boundedness is adversarially probed against widening
- parity exists across second-line surfaces for core permit meaning

**Residual limitation:**
- permit closure is strong at the release boundary, but not yet theorem-prover-complete in the formal-discharge sense

**Release status:** strong and materially valuable.

---

### 3.5 Canonicalization

**Current judgment:** materially strong but not maximally saturated.

**What is concretely aligned:**
- deterministic digest/canonical-bytes path exists
- equal-form collapse and anti-collapse probes exist
- idempotence probe exists for the current request surface
- parity exists across Python and Node.js surfaces for current canonicalization families

**Residual limitation:**
- canonicalization is strongest on the current request/bundle digest surfaces
- not every object family named abstractly in the object model has yet received equally broad adversarial canonicalization subfamilies

**Release status:** strong for current realized surfaces, but still one of the clearest remaining expansion zones.

---

### 3.6 No-bypass

**Current judgment:** strong executable-witness alignment.

**What is concretely aligned:**
- explicit non-bypass refusal exists
- adversarial bypass probes exist for direct/unsealed entry paths
- no detached release object is emitted outside lawful permit realization

**Residual limitation:**
- this is primitive-law and release-surface no-bypass, not OS-rooted or hardware-rooted enforcement

**Release status:** strong within primitive scope.

---

### 3.7 Theorem-family corpus closure

**Current judgment:** strong executable witness layer.

**What is concretely aligned:**
- every theorem family has a dedicated corpus family
- theorem-family harness exists
- theorem-family closure now also includes adversarial closure evidence and parity evidence

**Residual limitation:**
- theorem-family corpus coverage is executable witness evidence, not direct formal proof discharge

**Release status:** strong and important.

---

### 3.8 Second-implementation parity

**Current judgment:** clear upgrade and major value increase.

**What is concretely aligned:**
- independent Python second line
- externalized Python second line
- out-of-family Node.js second line
- parity harnesses across verification, runtime allow/refusal, and replay surfaces
- Node.js verification-subfamily parity exists on adversarial defect families

**Residual limitation:**
- the Node.js line is out-of-family and genuinely valuable, but still packaged within the same release line rather than as a separately governed repository/toolchain family

**Release status:** high-value upgrade.

---

### 3.9 Theorem-discharge evidence coupling

**Current judgment:** useful and strong, but wording must stay disciplined.

**What is concretely aligned:**
- theorem families are tied to executable witnesses
- theorem families are tied to corpus families
- theorem families are tied to adversarial and parity reports
- ledger artifacts exist in `PROOFS/`, `dist/`, and `REPORTS/`

**Residual limitation:**
- this is an executable-witness discharge ledger
- it is not a mechanized theorem-prover discharge ledger

**Release status:** strong, but must be read with exact truthfulness.

---

## 4. What this release line now truthfully supports

This release line truthfully supports the following claims:

1. it contains one ordered normative law family for the primitive
2. it contains multiple executable realization surfaces aligned against that law family
3. it contains structured permit/refusal/verification outputs
4. it contains theorem-family corpus witnesses
5. it contains adversarial closure witnesses
6. it contains verification-subfamily adversarial completion witnesses
7. it contains cross-surface and cross-line parity checks, including an out-of-family Node.js line
8. it contains an executable-witness theorem-discharge ledger

---

## 5. What this release line does not truthfully claim

This release line does **not** truthfully claim:

1. full theorem-prover discharge of theorem families
2. full object-family-wide canonicalization saturation for every abstract family named in the object model
3. a separately governed second repository with independent CI and governance
4. OS-level, kernel-level, or hardware-level non-bypass guarantees
5. universal external correctness, legality, truth, or safety

Any stronger reading would exceed the release truth boundary.

---

## 6. Exact residual gaps after finalization

The largest remaining concrete gaps are now:

1. broader object-family canonicalization saturation beyond the strongest current request/bundle digest surfaces
2. a separately governed out-of-repo second implementation line with independent toolchain/CI/governance
3. mechanized theorem discharge beyond executable-witness discharge
4. deeper adversarial saturation on every abstract object family if maximal closure is desired

These are no longer hidden. They are the explicit remaining heavy steps.

---

## 7. Final alignment judgment

The current release line is:

- materially upgraded
- high-level and non-trivial
- explicitly specified
- executable-witness rich
- parity-rich
- adversarially exercised
- more coherent than prior lines

It is **not yet absolute end-state closure**, but it is a substantially stronger and more truthful primitive release family than the earlier passes.
