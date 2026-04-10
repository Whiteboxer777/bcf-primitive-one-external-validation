from __future__ import annotations
import json
import hashlib
from pathlib import Path
from typing import Any

from .semantic_core import enumerate_states, admit, verify_boundary, permit_possible

ROOT = Path(__file__).resolve().parent.parent


def canonical_bytes(data: Any) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def digest_data(data: Any) -> str:
    return hashlib.sha256(canonical_bytes(data)).hexdigest()


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding='utf-8'))


def _canonicalization_subset() -> dict[str, Any]:
    cdir = ROOT / 'corpus' / 'canonicalization'
    a = load_json(cdir / 'request_semantically_equal_a.json')
    b = load_json(cdir / 'request_semantically_equal_b.json')
    d = load_json(cdir / 'request_distinct.json')
    ca = canonical_bytes(a)
    cb = canonical_bytes(b)
    cd = canonical_bytes(d)
    return {
        'equal_pair_same_bytes': ca == cb,
        'equal_pair_same_digest': digest_data(a) == digest_data(b),
        'distinct_pair_distinct_bytes': ca != cd,
        'idempotence_a': canonical_bytes(json.loads(ca.decode('utf-8'))) == ca,
        'idempotence_b': canonical_bytes(json.loads(cb.decode('utf-8'))) == cb,
        'idempotence_d': canonical_bytes(json.loads(cd.decode('utf-8'))) == cd,
        'digests': {
            'equal_a': digest_data(a),
            'equal_b': digest_data(b),
            'distinct': digest_data(d),
        },
    }


def run_mechanized_kernel_check() -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    counters = {
        'states_checked': 0,
        'allow_states': 0,
        'refusal_states': 0,
    }
    for state in enumerate_states():
        counters['states_checked'] += 1
        verdict = admit(state)
        if verdict == 'ALLOW':
            counters['allow_states'] += 1
        else:
            counters['refusal_states'] += 1
        if verdict not in {'ALLOW', 'REFUSAL'}:
            failures.append({'theorem': 'K1', 'reason': 'bad verdict universe', 'state': state.to_dict(), 'observed': verdict})
        if verify_boundary(state) != 'VERIFIED' and verdict == 'ALLOW':
            failures.append({'theorem': 'K2', 'reason': 'allow without verified boundary', 'state': state.to_dict()})
        core = [
            state.primitive_valid,
            state.bundle_valid,
            state.manifest_satisfied,
            state.verification_succeeded,
            state.request_valid,
            state.shape_satisfied,
            state.bounds_satisfied,
            state.contract_satisfied,
            state.action_binding_satisfied,
            state.witness_satisfied,
            state.no_fail_closed_trigger,
        ]
        if (not all(core)) and verdict == 'ALLOW':
            failures.append({'theorem': 'K3', 'reason': 'allow despite failed core predicate', 'state': state.to_dict()})
        expected = 'ALLOW' if all(core) and state.official_positive_path else 'REFUSAL'
        if verdict != expected:
            failures.append({'theorem': 'K4', 'reason': 'biconditional mismatch', 'state': state.to_dict(), 'expected': expected, 'observed': verdict})
        if not state.official_positive_path and permit_possible(state):
            failures.append({'theorem': 'K5', 'reason': 'permit possible without official path', 'state': state.to_dict()})
    c14n = _canonicalization_subset()
    for k in ['equal_pair_same_bytes', 'equal_pair_same_digest', 'distinct_pair_distinct_bytes', 'idempotence_a', 'idempotence_b', 'idempotence_d']:
        if not c14n[k]:
            failures.append({'theorem': 'K6', 'reason': f'canonicalization subset check failed: {k}'})
    return {
        'overall_ok': not failures,
        'kernel_scope': [
            'K1 verdict universe / totality core',
            'K2 verification necessity core',
            'K3 fail-closed core',
            'K4 admission biconditional core',
            'K5 no-bypass core',
            'K6 canonicalization determinism/idempotence subset core',
        ],
        'counters': counters,
        'canonicalization_subset': c14n,
        'failures': failures,
        'limits': [
            'This is a finite-state mechanized semantic kernel, not a full theorem prover discharge.',
            'The canonicalization theorem coverage is subset-scoped to the dedicated request corpus fixtures.',
            'The checker witnesses the semantic kernel and preparation surface for later formal mechanization.',
        ],
    }
