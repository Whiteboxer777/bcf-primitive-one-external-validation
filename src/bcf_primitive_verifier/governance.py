"""Facade over the canonical frozen trust kernel.

This module deliberately exposes the stable trust-kernel implementation from
`bcf_trust_kernel.governance` so the primary and verifier packages share only the
minimal frozen kernel surface rather than importing each other.
"""
from bcf_trust_kernel.governance import *  # noqa: F401,F403
