# `SPEC/WITNESS_CERTIFICATE_EXPANSION_EXECUTABLE_CONTRACT.md`

This executable contract fixes the witness-certificate expansion line.

The controlling artifacts are:

- `SPEC/WITNESS_CERTIFICATE_EXPANSION.md`
- `schemas/witness_certificate.schema.json`
- `tools/witness_certificate_expansion_gate.py`
- `dist/witness_certificate_expansion_report.json`

The current line is satisfied only if:

1. witness certificates carry the expanded version/scope/source-kind discipline
2. bundle sample witness artifacts exist for verification, permit, refusal, replay allow, replay refusal, and non-bypass refusal
3. primary, independent, externalized, and Node runtime/replay/verification surfaces emit schema-valid digest-bound witness certificates on the current kernel corpus
4. the witness-certificate expansion gate returns `overall_ok = true`

This contract is scoped executable-witness discipline. It is not theorem-prover-grade witness-certificate closure.
