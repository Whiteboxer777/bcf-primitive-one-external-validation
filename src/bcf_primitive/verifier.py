"""Runtime-facing facade to the official verifier surface.

The authoritative verifier implementation lives in `bcf_primitive_verifier`.
The primary package exposes this facade only for compatibility; no separate
verifier logic is maintained here.
"""
from bcf_primitive_verifier.verifier import *  # noqa: F401,F403
