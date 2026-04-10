# BCF Primitive One — External Validation Acceptance Criteria

## What Must Be True for This Run to Be Valid

### 1. Environment
- Python 3.11 or higher
- Node.js 18 or higher (required for Node out-of-family parity; falls back to pre-generated cache if absent)
- `cryptography>=42` and `jsonschema>=4.0` installed
- Fresh checkout — no prior build artifacts in `dist/`

### 2. Gate Execution
Run exactly:
```
PYTHONPATH=src PYTHONDONTWRITEBYTECODE=1 python tools/external_truth_closure_gate.py
```

### 3. Required Outputs
After a successful run, the following files must exist:
- `dist/EXTERNAL_TRUTH_VERDICT.json`
- `dist/EXTERNAL_TRUTH_CHAIN.json`
- `dist/external_digest_reconciliation_report.json`

### 4. Required Verdict Fields
`dist/EXTERNAL_TRUTH_VERDICT.json` must satisfy ALL of:

| Field | Required Value |
|-------|----------------|
| `overall_ok` | `true` |
| `verdict` | `"EXTERNAL_TRUTH_CLOSED_INTERNAL_CLEAN_ROOM"` |
| `artifact_id` | `"BCF_PRIMITIVE_ONE_EXTERNAL_TRUTH_CLOSURE"` |
| `parity_outcomes.independent_overall` | `true` |
| `parity_outcomes.node_overall` | `true` |
| `proof_outcome.proof_ok` | `true` |
| `audit_outcome.overall_ok` | `true` |
| `hygiene_outcome.overall_ok` | `true` |
| `digest_reconciliation_outcome` | `true` |

### 5. Artifact Digests Are Authoritative
The following digest fields in `EXTERNAL_TRUTH_VERDICT.json` are SHA-256 hashes of immutable source files. A rerun on the same commit MUST produce identical digests:

- `trust_kernel_digests.bcf_trust_kernel_init`
- `verifier_digest_set.bcf_primitive_verifier_verifier`
- `runtime_digest_set.bcf_primitive_runtime`
- `independent_line_digest_set.bcf_primitive_independent_semantic_core`
- `node_line_digest_set.node_second_line_runtime`
- `bundle_digest`

If any digest changes between reruns on the same commit, the run is invalid.

### 6. Parity Must Hold Across All Cases
All entries in `parity_outcomes.independent_python` and `parity_outcomes.node_out_of_family` must be `true`.

## What This Does NOT Prove

- OS-level non-bypass (hardware/firmware isolation is out of scope)
- Separate-repo external hosted CI attestation (RG-04: pending)
- Full theorem-prover discharge over the complete family (RG-05: mechanized kernel is scoped)
