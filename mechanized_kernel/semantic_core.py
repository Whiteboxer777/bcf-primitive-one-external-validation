from __future__ import annotations
from dataclasses import dataclass, asdict
from itertools import product
from typing import Iterable

@dataclass(frozen=True)
class KernelState:
    primitive_valid: bool
    bundle_valid: bool
    manifest_satisfied: bool
    verification_succeeded: bool
    request_valid: bool
    shape_satisfied: bool
    bounds_satisfied: bool
    contract_satisfied: bool
    action_binding_satisfied: bool
    witness_satisfied: bool
    no_fail_closed_trigger: bool
    official_positive_path: bool

    def to_dict(self) -> dict[str, bool]:
        return asdict(self)


def admit(state: KernelState) -> str:
    ok = (
        state.primitive_valid
        and state.bundle_valid
        and state.manifest_satisfied
        and state.verification_succeeded
        and state.request_valid
        and state.shape_satisfied
        and state.bounds_satisfied
        and state.contract_satisfied
        and state.action_binding_satisfied
        and state.witness_satisfied
        and state.no_fail_closed_trigger
        and state.official_positive_path
    )
    return "ALLOW" if ok else "REFUSAL"


def verify_boundary(state: KernelState) -> str:
    ok = (
        state.primitive_valid
        and state.bundle_valid
        and state.manifest_satisfied
        and state.verification_succeeded
        and state.no_fail_closed_trigger
    )
    return "VERIFIED" if ok else "NOT_VERIFIED"


def permit_possible(state: KernelState) -> bool:
    return admit(state) == "ALLOW" and state.official_positive_path


def enumerate_states() -> Iterable[KernelState]:
    for bits in product([False, True], repeat=12):
        yield KernelState(*bits)
