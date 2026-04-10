from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .admission_normal_form import AdmissionNormalForm, compile_admission_normal_form
from .common import digest_data
from .kernel_support import Profile, parse_node


@dataclass(frozen=True)
class CompiledClause:
    clause_id: str
    positive_atoms: tuple[str, ...]
    negative_atoms: tuple[str, ...]
    literal_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            'clause_id': self.clause_id,
            'positive_atoms': list(self.positive_atoms),
            'negative_atoms': list(self.negative_atoms),
            'literal_count': self.literal_count,
        }


@dataclass(frozen=True)
class CompiledBackend:
    profile_id: str
    source_kind: str
    anf_digest: str
    atom_index: tuple[dict[str, Any], ...]
    clauses: tuple[CompiledClause, ...]
    literal_index: dict[str, tuple[str, ...]]
    evaluation_order: tuple[str, ...]
    compilation_trace: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        body = {
            'profile_id': self.profile_id,
            'source_kind': self.source_kind,
            'anf_digest': self.anf_digest,
            'atom_index': list(self.atom_index),
            'clauses': [c.to_dict() for c in self.clauses],
            'literal_index': {k: list(v) for k, v in sorted(self.literal_index.items())},
            'evaluation_order': list(self.evaluation_order),
            'compilation_trace': list(self.compilation_trace),
        }
        body['backend_digest'] = digest_data(body)
        return body


def _lit_key(atom_id: str, polarity: bool) -> str:
    return f'{atom_id}:{"+" if polarity else "-"}'


def compile_compiled_backend(profile: Profile) -> CompiledBackend:
    anf = compile_admission_normal_form(profile)
    anf_dict = anf.to_dict()
    clauses: list[CompiledClause] = []
    literal_index: dict[str, list[str]] = {}
    for idx, clause in enumerate(anf.clauses, start=1):
        clause_id = f'C{idx:04d}'
        pos = tuple(sorted(l.atom_id for l in clause.literals if l.polarity))
        neg = tuple(sorted(l.atom_id for l in clause.literals if not l.polarity))
        compiled = CompiledClause(clause_id=clause_id, positive_atoms=pos, negative_atoms=neg, literal_count=len(clause.literals))
        clauses.append(compiled)
        for lit in clause.literals:
            literal_index.setdefault(_lit_key(lit.atom_id, lit.polarity), []).append(clause_id)
    stable_index = {k: tuple(sorted(v)) for k, v in sorted(literal_index.items())}
    evaluation_order = tuple(entry['atom_id'] for entry in anf_dict['atom_index'])
    trace = tuple(anf.compilation_trace) + ('compiled-backend-index', f'compiled-clause-count={len(clauses)}', f'compiled-atom-count={len(evaluation_order)}')
    return CompiledBackend(
        profile_id=anf.profile_id,
        source_kind='indexed_dnf_clause_backend_v1',
        anf_digest=anf_dict['anf_digest'],
        atom_index=tuple(anf_dict['atom_index']),
        clauses=tuple(clauses),
        literal_index=stable_index,
        evaluation_order=evaluation_order,
        compilation_trace=trace,
    )


def _atom_truth_map(compiled: CompiledBackend, request: dict[str, Any]) -> dict[str, bool]:
    from .kernel_support import EvalContext, atom_outcome

    obj = request.get('object', request)
    ctx = EvalContext(
        obj=obj,
        authority=request.get('authority', {}),
        trust=request.get('trust', {}),
        regime=request.get('regime', {}),
        evidence=request.get('evidence', {}),
        action=request.get('action', {}),
        before=request.get('before', {}),
        after=request.get('after', request.get('after', obj)),
    )
    truth: dict[str, bool] = {}
    for entry in compiled.atom_index:
        atom = parse_node(entry['atom'])
        ok, _, _ = atom_outcome(atom, ctx)
        truth[entry['atom_id']] = ok
    return truth


def evaluate_compiled_backend(compiled: CompiledBackend, request: dict[str, Any]) -> dict[str, Any]:
    truth = _atom_truth_map(compiled, request)
    alive = {clause.clause_id for clause in compiled.clauses}
    satisfied_counts = {clause.clause_id: 0 for clause in compiled.clauses}
    clause_map = {clause.clause_id: clause for clause in compiled.clauses}
    elimination_trace: list[dict[str, Any]] = []

    for atom_id in compiled.evaluation_order:
        atom_value = truth[atom_id]
        contradictory_key = _lit_key(atom_id, not atom_value)
        supportive_key = _lit_key(atom_id, atom_value)
        removed = []
        for clause_id in compiled.literal_index.get(contradictory_key, ()):  # prune impossible clauses
            if clause_id in alive:
                alive.remove(clause_id)
                removed.append(clause_id)
        for clause_id in compiled.literal_index.get(supportive_key, ()):  # count satisfied literals on surviving clauses
            if clause_id in alive:
                satisfied_counts[clause_id] += 1
        if removed or compiled.literal_index.get(supportive_key):
            elimination_trace.append({
                'atom_id': atom_id,
                'atom_truth': atom_value,
                'removed_clauses': sorted(removed),
                'supportive_clause_hits': list(compiled.literal_index.get(supportive_key, ())),
                'alive_clause_count': len(alive),
            })
        for clause_id in list(alive):
            if satisfied_counts[clause_id] == clause_map[clause_id].literal_count:
                return {
                    'verdict': 'ALLOW',
                    'matched_clause_id': clause_id,
                    'alive_clause_count': len(alive),
                    'atom_truth': truth,
                    'elimination_trace': elimination_trace,
                }

    return {
        'verdict': 'REFUSAL',
        'matched_clause_id': None,
        'alive_clause_count': len(alive),
        'atom_truth': truth,
        'elimination_trace': elimination_trace,
    }
