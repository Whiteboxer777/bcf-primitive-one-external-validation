# EXTERNAL TRUTH CLOSURE CONTRACT

## Objective

The release must be rerunnable from a clean-room copy of the canonical surface and produce one authoritative external truth chain.

## Mandatory checks

1. Bundle verification succeeds on the canonical invoice bundle.
2. One-shot proof succeeds on canonical allow/deny requests.
3. External audit succeeds, including tamper, missing-file, non-bypass, and oversize refusal checks.
4. Primary runtime/verifier surface matches the independent Python implementation on canonical cases.
5. Primary runtime/verifier surface matches the out-of-family Node implementation on canonical cases.
6. Digest reconciliation across the above surfaces succeeds.
7. Final tree passes artifact hygiene gate.

## Required outputs

- `dist/EXTERNAL_TRUTH_CHAIN.json`
- `dist/EXTERNAL_TRUTH_VERDICT.json`
- `dist/external_digest_reconciliation_report.json`

## Non-claims

- no OS/hardware non-bypass claim
- no separate-repo attestation claim in this pass
- no whole-family theorem-prover closure claim in this pass
