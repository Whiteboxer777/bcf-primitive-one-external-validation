# PROOF_OBLIGATIONS

This file states the exact proof obligations of the current mechanized-kernel pass.

## PO-K1
For every kernel state in the finite abstract semantic domain, the admission reducer returns exactly one verdict in `{ALLOW, REFUSAL}`.

## PO-K2
For every kernel state in the finite abstract semantic domain, if the verification reducer is not `VERIFIED`, then the admission reducer is not `ALLOW`.

## PO-K3
For every kernel state in the finite abstract semantic domain, if any mandatory core admission predicate is false, then final admission is not `ALLOW`.

## PO-K4
For every kernel state in the finite abstract semantic domain, final admission is exactly equivalent to the conjunction of all mandatory core predicates plus official-positive-path truth.

## PO-K5
For every kernel state in the finite abstract semantic domain, no permit is possible when the official positive path flag is false.

## PO-K6
For the dedicated canonicalization subset corpus, canonicalization is deterministic on the equal pair, non-collapsing on the distinct pair, and idempotent on the canonicalized output.

## Explicit limit
These proof obligations do not claim to discharge the entire primitive family. They define the exact core theorem kernel mechanized in this pass.
