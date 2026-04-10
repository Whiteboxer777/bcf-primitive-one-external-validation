# Verifier Trusted Computing Base

Verifier trust root is now frozen through `src/bcf_trust_kernel/` plus the verifier-only verification logic in `src/bcf_primitive_verifier/`.

The verifier surface must not import `bcf_primitive`.
