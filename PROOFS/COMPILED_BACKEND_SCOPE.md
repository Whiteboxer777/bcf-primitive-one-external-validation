# COMPILED_BACKEND_SCOPE

The compiled-backend family is kernel-scoped.

It currently covers:
- ANF-derived indexed backend compilation
- deterministic recompilation
- parity with ANF on current kernel corpus
- parity with reference evaluator on current kernel corpus
- compiler/verifier artifact recomputation

It does not yet cover:
- whole-family final IR
- whole-family backend semantics
- solver lowering correctness
- whole-family mechanized theorem discharge
