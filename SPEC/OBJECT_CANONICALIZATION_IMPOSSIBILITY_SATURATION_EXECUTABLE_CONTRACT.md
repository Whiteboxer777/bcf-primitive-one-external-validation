# `SPEC/OBJECT_CANONICALIZATION_IMPOSSIBILITY_SATURATION_EXECUTABLE_CONTRACT.md`

This executable contract fixes the machine-checked surfaces for the object/canonicalization/impossibility saturation pass.

## Required executable surface

- `tools/object_canonicalization_impossibility_saturation_gate.py`

## Required report artifacts

- `dist/object_canonicalization_impossibility_saturation_report.json`
- `REPORTS/object_canonicalization_impossibility_saturation_report.json`

## Required witness classes

### Object model
- verification result schema validity
- permit schema validity
- refusal schema validity
- witness certificate schema validity
- schema-negative mutations proving required-field blocking and malformed-object rejection

### Canonicalization
- request pair equality/distinctness
- action pair equality/distinctness
- generic object equality/distinctness
- idempotence for these surfaces

### Impossibility
- no allow without verification
- no permit on refusal
- no third final verdict
- no bypass positive authority
- invalid action descriptor refusal

## Truth boundary

This contract raises executable witness strength for object-model, canonicalization, and impossibility families within the current primitive line. It does not claim whole-family theorem-prover-grade discharge.
