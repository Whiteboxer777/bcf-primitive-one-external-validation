# BCF Primitive One — Trust Boundary Matrix

This matrix freezes the authoritative release surface after the independence-closure pass.

| Path | Authority level | Role | Verdict trust | Runtime trust | Independent surface | Replaceable | Release surface |
|---|---|---|---:|---:|---:|---:|---|
| `src/bcf_trust_kernel` | `trust_kernel` | frozen minimal shared kernel | yes | yes | no | no | `canonical` |
| `src/bcf_primitive_verifier` | `verifier_surface` | official bundle verifier surface | yes | no | no | no | `canonical` |
| `src/bcf_primitive` | `runtime_surface` | official compile/runtime/sealed execution surface | no | yes | no | no | `canonical` |
| `src/bcf_primitive_independent` | `independent_parity_surface` | clean-room parity implementation | no | no | yes | yes | `canonical` |
| `node_second_line` | `out_of_family_parity_surface` | language-separated second line parity surface | no | no | yes | yes | `canonical` |
| `externalized_second_line` | `externalized_parity_surface` | externalized Python parity/export surface | no | no | yes | yes | `canonical` |
| `mechanized_kernel` | `mechanization_prep` | mechanized proof preparation surface | no | no | no | yes | `auxiliary` |
| `SPEC` | `law_and_contract_surface` | normative law, contracts, and closure matrices | yes | yes | no | no | `canonical` |
| `PROOFS` | `proof_mapping_surface` | scope statements and theorem maps | no | no | no | yes | `auxiliary` |
| `tools` | `gate_and_audit_surface` | machine gates, harnesses, release audits | no | no | no | yes | `canonical` |
| `tests` | `test_surface` | local regression and corpus execution checks | no | no | no | yes | `auxiliary` |
| `dist` | `derived_release_artifacts` | generated reports and export bundles | no | no | no | yes | `canonical` |

Canonical release surface = trust kernel + official verifier + official runtime/compiler + parity surfaces + law/contracts + machine gates + derived canonical reports.
Auxiliary surface = proof-prep, test-only, and support layers not required to trust a verdict.
