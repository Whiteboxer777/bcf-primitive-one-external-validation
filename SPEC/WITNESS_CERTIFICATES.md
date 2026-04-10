# `SPEC/WITNESS_CERTIFICATES.md`

## 0. Status

This document defines the kernel-scoped witness-certificate line for BCF Primitive One.

Its function is to define explicit, schema-closed, digest-bound witness certificates attached to verification results, permits, and refusals.

This line is preparation-scope and evidence-carrying. It does not claim whole-family proof certificates or theorem-prover discharge.

## 1. Purpose

Witness certificates exist so that primitive outputs carry compact, verifiable evidence objects rather than only raw structured decisions.

For the current line, three witness certificate families are required:

- `verification_witness`
- `permit_witness`
- `refusal_witness`

Each certificate binds:

- primitive identity
- source verdict class
- bundle/request/action digests where applicable
- source output digest
- certificate digest
- scoped witness claims

## 2. Current scope

The current witness-certificate line is kernel-scoped. It guarantees:

- schema-closed witness certificate structure
- deterministic source-digest binding to verification/permit/refusal outputs
- compiler emission of sample witness certificates inside canonical bundles
- verifier checking of witness-certificate schema presence and certificate internal integrity
- runtime attachment of witness certificates to primary outputs

It does not yet claim:

- whole-family proof certificates
- minimal unsat proofs
- proof-carrying backend certificates
- cross-family theorem-prover certificates

## 3. Expanded current line

The current evidence-carrying line now also requires:

- explicit certificate version and certificate scope
- explicit source-kind distinction
- explicit binding digest
- explicit claim-set digest
- sample bundle artifacts for replay allow, replay refusal, and non-bypass refusal
- witness parity across primary, independent, externalized, and Node runtime/replay/verification surfaces on the current kernel corpus
