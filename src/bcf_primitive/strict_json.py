"""Facade over the canonical frozen trust kernel.

This module deliberately exposes the stable trust-kernel implementation from
`bcf_trust_kernel.strict_json` so the primary and verifier packages share only the
minimal frozen kernel surface rather than importing each other.
"""
from bcf_trust_kernel.strict_json import *  # noqa: F401,F403
