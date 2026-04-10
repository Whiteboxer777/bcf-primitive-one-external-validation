# MECHANIZED_KERNEL_SCOPE

Status: normative preparation document for the mechanized-kernel pass.

This file fixes the exact scope of mechanization attempted in the current pass.

## Included theorem kernel

The current mechanized kernel deliberately covers only the smallest highest-value theorem core:

- K1 verdict universe / totality core
- K2 verification necessity core
- K3 fail-closed core
- K4 admission biconditional core
- K5 no-bypass core
- K6 canonicalization determinism / idempotence core for a dedicated request subset

## Excluded from current mechanized kernel

The following remain outside this mechanized kernel pass:

- full object-model mechanization
- full refusal-algebra mechanization
- full permit-algebra mechanization
- full theorem-family mechanization
- full executable adequacy proof of every implementation surface
- full cross-language theorem-prover-grade parity proof

## Exact interpretation boundary

The current pass is a mechanized-kernel preparation and execution pass. It is stronger than prose-only or corpus-only discipline, but it does **not** claim full theorem-prover discharge of the entire primitive family.
