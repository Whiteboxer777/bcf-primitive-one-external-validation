# Equivalence corpus

This corpus fixes the minimal second-surface parity target for BCF Primitive One.

Cases:
- `allow_request.json` must yield parity between the runtime release surface and the verifier replay surface at the decision-class boundary.
- `deny_request.json` must yield parity between the runtime release surface and the verifier replay surface at the decision-class boundary.

Parity dimensions:
- primitive identity
- bundle digest
- request digest
- decision class (`ALLOW` vs `REFUSAL`)
- schema-valid runtime output
- schema-valid verifier-side refusal output where refusal occurs
