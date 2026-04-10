# WHOLE_FAMILY_MECHANIZATION_EXPANSION_EXECUTABLE_CONTRACT

## Status

This document defines the executable contract for the whole-family mechanization expansion line.

The controlling executable surfaces are:
- `tools/whole_family_mechanization_expansion_gate.py`
- `dist/whole_family_mechanization_expansion_report.json`
- supporting gate reports for:
  - mechanized kernel
  - ANF
  - compiled backend
  - witness certificates

## Contract claims

The contract claims only the following:
- the current mechanized kernel, ANF line, compiled backend line, and witness-certificate line are executable-witness coherent on the kernel-scoped canonical corpus
- fail-closed and no-bypass preservation remain visible at this cross-layer boundary
- the report emitted by the gate is the authoritative executable witness for this expansion line

The contract does **not** claim:
- whole-family theorem-prover discharge
- full backend correctness beyond current scope
- saturation of every object family or canonicalization family
- elimination of the residual RC gaps already declared elsewhere
