"""Facade over the canonical frozen trust kernel.

This module intentionally re-exports the authoritative implementation from
`bcf_trust_kernel.admission_normal_form` so that duplicated semantic logic does not exist across the
primary and verifier families.
"""
from bcf_trust_kernel.admission_normal_form import *  # noqa: F401,F403
