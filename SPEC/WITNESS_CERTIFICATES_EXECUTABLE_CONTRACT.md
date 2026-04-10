# `SPEC/WITNESS_CERTIFICATES_EXECUTABLE_CONTRACT.md`

## 0. Status

This document defines the executable contract for the witness-certificate line.

## 1. Contract surfaces

Normative prose:
- `SPEC/WITNESS_CERTIFICATES.md`

Machine-readable schema:
- `schemas/witness_certificate.schema.json`

Executable builder/attacher:
- `src/bcf_primitive_verifier/witness_certificate.py`

Executable gate:
- `tools/witness_certificate_gate.py`

Audit artifacts:
- `REPORTS/witness_certificate_gate_report.json`
- `dist/witness_certificate_gate_report.json`

## 2. Required executable properties

The current line requires:

- witness certificate schema validity
- deterministic certificate digest recomputation
- deterministic source digest recomputation against verification/permit/refusal payloads
- bundle emission of sample witness certificate artifacts
- verifier detection of missing or invalid witness-certificate schema/artifacts

## 3. Truth boundary

This contract does not claim whole-family certificate completeness. It claims kernel-scoped, schema-closed, digest-bound executable witness certificates for the current primary evidence-carrying line.

## Expansion coupling

The witness-certificate preparation line is extended by `SPEC/WITNESS_CERTIFICATE_EXPANSION.md` and `tools/witness_certificate_expansion_gate.py`. The expansion line requires green witness parity and expanded sample witness artifacts on the current implemented family scope.
