
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any

from .common import canonical_bytes, digest_data
from .kernel_support import Node, Profile, normalize

ATOM_KINDS = {
    'TRUE','FALSE','EQ','NEQ','IN','NOT_IN','EXISTS','ABSENT','RANGE','MATCHES',
    'AUTHORITY_EQ','TRUST_EQ','REGIME_EQ','EVIDENCE_EQ','ACTION_EQ',
    'BEFORE_EQ','AFTER_EQ','BEFORE_RANGE','AFTER_RANGE','CHANGED','UNCHANGED',
}


def _sort_key(node: Node) -> tuple:
    return (
        node.kind,
        node.path or '',
        repr(node.value),
        repr(node.low),
        repr(node.high),
        tuple(sorted(node.metadata)),
        tuple(_sort_key(c) for c in node.children),
    )


def _node_dict(node: Node) -> dict[str, Any]:
    return node.to_dict()


@dataclass(frozen=True)
class Literal:
    atom_id: str
    polarity: bool
    atom: Node

    def to_dict(self) -> dict[str, Any]:
        return {
            'atom_id': self.atom_id,
            'polarity': 'positive' if self.polarity else 'negative',
            'atom': _node_dict(self.atom),
        }


@dataclass(frozen=True)
class Clause:
    literals: tuple[Literal, ...]

    def to_dict(self) -> dict[str, Any]:
        return {'literals': [lit.to_dict() for lit in self.literals]}


@dataclass(frozen=True)
class AdmissionNormalForm:
    profile_id: str
    source_kind: str
    normalized_root: dict[str, Any]
    atom_index: tuple[dict[str, Any], ...]
    clauses: tuple[Clause, ...]
    compilation_trace: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            'profile_id': self.profile_id,
            'source_kind': self.source_kind,
            'normalized_root': self.normalized_root,
            'atom_index': list(self.atom_index),
            'clauses': [c.to_dict() for c in self.clauses],
            'compilation_trace': list(self.compilation_trace),
            'anf_digest': digest_data({
                'profile_id': self.profile_id,
                'source_kind': self.source_kind,
                'normalized_root': self.normalized_root,
                'atom_index': list(self.atom_index),
                'clauses': [c.to_dict() for c in self.clauses],
                'compilation_trace': list(self.compilation_trace),
            }),
        }


def _is_atom(node: Node) -> bool:
    return node.kind in ATOM_KINDS


def to_nnf(node: Node) -> Node:
    if _is_atom(node):
        return node
    if node.kind == 'NOT':
        child = node.children[0]
        if child.kind == 'TRUE':
            return Node('FALSE')
        if child.kind == 'FALSE':
            return Node('TRUE')
        if child.kind == 'NOT':
            return to_nnf(child.children[0])
        if child.kind == 'AND':
            return Node('OR', children=tuple(to_nnf(Node('NOT', children=(c,))) for c in child.children))
        if child.kind == 'OR':
            return Node('AND', children=tuple(to_nnf(Node('NOT', children=(c,))) for c in child.children))
        return Node('NOT', children=(child,), metadata=node.metadata)
    if node.kind in {'AND','OR'}:
        return Node(node.kind, children=tuple(to_nnf(c) for c in node.children), metadata=node.metadata)
    return node


def _collect_atoms(node: Node) -> list[Node]:
    out: list[Node] = []
    def walk(n: Node) -> None:
        if _is_atom(n):
            out.append(n)
            return
        if n.kind == 'NOT' and n.children and _is_atom(n.children[0]):
            out.append(n.children[0])
            return
        for c in n.children:
            walk(c)
    walk(node)
    uniq = []
    seen = set()
    for a in sorted(out, key=_sort_key):
        key = _sort_key(a)
        if key not in seen:
            seen.add(key)
            uniq.append(a)
    return uniq


def _literal_from_node(node: Node, atom_id_map: dict[tuple, str]) -> Literal:
    if node.kind == 'NOT':
        atom = node.children[0]
        return Literal(atom_id_map[_sort_key(atom)], False, atom)
    return Literal(atom_id_map[_sort_key(node)], True, node)


def _merge_clause_sets(left: list[list[Literal]], right: list[list[Literal]]) -> list[list[Literal]]:
    merged: list[list[Literal]] = []
    for a in left:
        for b in right:
            combo = list(a) + list(b)
            index: dict[str, bool] = {}
            bad = False
            deduped: list[Literal] = []
            for lit in combo:
                if lit.atom_id in index:
                    if index[lit.atom_id] != lit.polarity:
                        bad = True
                        break
                    continue
                index[lit.atom_id] = lit.polarity
                deduped.append(lit)
            if not bad:
                deduped = sorted(deduped, key=lambda l: (l.atom_id, not l.polarity))
                merged.append(deduped)
    return merged


def _dnf(node: Node, atom_id_map: dict[tuple, str]) -> list[list[Literal]]:
    if node.kind == 'TRUE':
        return [[]]
    if node.kind == 'FALSE':
        return []
    if _is_atom(node) or (node.kind == 'NOT' and node.children and _is_atom(node.children[0])):
        return [[_literal_from_node(node, atom_id_map)]]
    if node.kind == 'OR':
        out: list[list[Literal]] = []
        for child in node.children:
            out.extend(_dnf(child, atom_id_map))
        return out
    if node.kind == 'AND':
        clauses = [[]]
        for child in node.children:
            clauses = _merge_clause_sets(clauses, _dnf(child, atom_id_map))
        return clauses
    raise ValueError(f'Unsupported node kind for ANF compilation: {node.kind}')


def compile_admission_normal_form(profile: Profile) -> AdmissionNormalForm:
    norm = normalize(profile.root)
    nnf = to_nnf(norm.node)
    atoms = _collect_atoms(nnf)
    atom_entries: list[dict[str, Any]] = []
    atom_id_map: dict[tuple, str] = {}
    for idx, atom in enumerate(atoms, start=1):
        atom_id = f'A{idx:04d}'
        atom_id_map[_sort_key(atom)] = atom_id
        atom_entries.append({
            'atom_id': atom_id,
            'atom_kind': atom.kind,
            'rule_id': dict(atom.metadata).get('rule_id'),
            'atom': _node_dict(atom),
            'atom_digest': hashlib.sha256(canonical_bytes(_node_dict(atom))).hexdigest(),
        })
    raw_clauses = _dnf(nnf, atom_id_map)
    stable = []
    seen = set()
    for lits in raw_clauses:
        key = tuple((lit.atom_id, lit.polarity) for lit in lits)
        if key in seen:
            continue
        seen.add(key)
        stable.append(Clause(tuple(lits)))
    stable = tuple(sorted(stable, key=lambda c: tuple((lit.atom_id, lit.polarity) for lit in c.literals)))
    trace = tuple(norm.trace) + ('to-nnf', 'dnf-compilation', f'clause-count={len(stable)}', f'atom-count={len(atom_entries)}')
    return AdmissionNormalForm(
        profile_id=profile.profile_id,
        source_kind='dnf_literal_clauses',
        normalized_root=norm.node.to_dict(),
        atom_index=tuple(atom_entries),
        clauses=stable,
        compilation_trace=trace,
    )


def evaluate_anf(anf: AdmissionNormalForm, profile: Profile, request: dict[str, Any]) -> dict[str, Any]:
    from .kernel_support import evaluate_profile, EvalContext, atom_outcome, select_scope, deep_get
    obj = request.get('object', request) if profile.mode == 'object' else request.get('after', request.get('object', {}))
    ctx = EvalContext(obj=obj, authority=request.get('authority', {}), trust=request.get('trust', {}), regime=request.get('regime', {}), evidence=request.get('evidence', {}), action=request.get('action', {}), before=request.get('before', {}), after=request.get('after', obj))
    atom_truth: dict[str, bool] = {}
    atom_nodes = {entry['atom_id']: entry['atom'] for entry in anf.atom_index}
    for entry in anf.atom_index:
        atom = Node(**{k:v for k,v in entry['atom'].items() if k in {'kind','path','value','low','high'}} , children=tuple(), metadata=tuple(sorted(entry['atom'].get('metadata', {}).items())))
        ok, _, _ = atom_outcome(atom, ctx)
        atom_truth[entry['atom_id']] = ok
    clause_results = []
    for clause in anf.clauses:
        clause_ok = all(atom_truth[lit.atom_id] if lit.polarity else (not atom_truth[lit.atom_id]) for lit in clause.literals)
        clause_results.append(clause_ok)
    verdict = 'ALLOW' if any(clause_results) or (not anf.clauses and anf.normalized_root.get('kind')=='TRUE') else 'REFUSAL'
    ref = evaluate_profile(profile, request)
    return {
        'verdict': verdict,
        'reference_verdict': 'ALLOW' if ref.verdict == 'ALLOW' else 'REFUSAL',
        'equivalent_to_reference': verdict == ('ALLOW' if ref.verdict == 'ALLOW' else 'REFUSAL'),
        'clause_results': clause_results,
        'atom_truth': atom_truth,
    }
