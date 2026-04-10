# `SPEC/WITNESS_CERTIFICATE_EXPANSION.md`

## 0. Status

This document defines the witness-certificate expansion line for BCF Primitive One.

Its function is to strengthen the existing witness-certificate preparation line into a broader executable-witness discipline covering:

- stricter witness-certificate structure
- replay and no-bypass witness artifacts
- multi-implementation witness parity on current implemented surfaces
- explicit witness-carrying sample bundle artifacts

This line remains scoped. It does not claim theorem-prover-grade proof certificates or whole-family minimal proof objects.

## 1. Purpose

Witness certificates are expanded so that the evidence-carrying line is no longer limited to only three minimal sample artifacts and one primary output family. The current expansion requires:

- deterministic witness certificate versioning and scope fields
- explicit source-kind distinction across verification, permit, refusal, replay-allow, replay-refusal, and non-bypass refusal
- explicit binding digests and claim-set digests
- sample bundle witness artifacts for replay and non-bypass paths
- witness parity checks across primary, independent, externalized, and Node second lines on the current implemented runtime/replay/verification surfaces

## 2. Truth boundary

This line guarantees executable witness expansion on the currently implemented family scope. It does not yet claim:

- compact minimal proof certificates
- clause-minimal unsat proof objects
- whole-family backend proof certificates
- theorem-prover-grade certificate soundness
