"""Independent semantic core for BCF Primitive One.

This module is a self-contained second semantic implementation family.
It does not import semantic operations from bcf_trust_kernel, bcf_primitive, or
bcf_primitive_verifier.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations, product
from typing import Any, Literal

from .strict_json import StrictParseError

NodeKind = Literal[
    'TRUE', 'FALSE', 'AND', 'OR', 'NOT',
    'EQ', 'NEQ', 'IN', 'NOT_IN', 'EXISTS', 'ABSENT',
    'RANGE', 'MATCHES',
    'AUTHORITY_EQ', 'TRUST_EQ', 'REGIME_EQ', 'EVIDENCE_EQ', 'ACTION_EQ',
    'BEFORE_EQ', 'AFTER_EQ', 'BEFORE_RANGE', 'AFTER_RANGE', 'CHANGED', 'UNCHANGED',
]
Mode = Literal['object', 'transition']
DomainKind = Literal['enum', 'bounded_int', 'bounded_decimal', 'boolean', 'regex_witness']
ALL_ATOMS = {
    'TRUE', 'FALSE', 'EQ', 'NEQ', 'IN', 'NOT_IN', 'EXISTS', 'ABSENT', 'RANGE', 'MATCHES',
    'AUTHORITY_EQ', 'TRUST_EQ', 'REGIME_EQ', 'EVIDENCE_EQ', 'ACTION_EQ',
    'BEFORE_EQ', 'AFTER_EQ', 'BEFORE_RANGE', 'AFTER_RANGE', 'CHANGED', 'UNCHANGED',
}
VERDICT_ALLOW = 'ALLOW'
VERDICT_DENY = 'DENY'


@dataclass(frozen=True)
class DomainSpec:
    kind: DomainKind
    values: tuple[Any, ...] = ()
    min: float | int | None = None
    max: float | int | None = None
    step: float | int | None = None
    matching: tuple[str, ...] = ()
    non_matching: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {'kind': self.kind}
        if self.values:
            data['values'] = list(self.values)
        if self.min is not None:
            data['min'] = self.min
        if self.max is not None:
            data['max'] = self.max
        if self.step is not None:
            data['step'] = self.step
        if self.matching:
            data['matching'] = list(self.matching)
        if self.non_matching:
            data['non_matching'] = list(self.non_matching)
        return data


@dataclass(frozen=True)
class Node:
    kind: NodeKind
    path: str | None = None
    value: Any = None
    low: Any = None
    high: Any = None
    children: tuple['Node', ...] = field(default_factory=tuple)
    metadata: tuple[tuple[str, Any], ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {'kind': self.kind}
        if self.path is not None:
            data['path'] = self.path
        if self.value is not None:
            data['value'] = self.value
        if self.low is not None:
            data['low'] = self.low
        if self.high is not None:
            data['high'] = self.high
        if self.children:
            data['children'] = [c.to_dict() for c in self.children]
        if self.metadata:
            data['metadata'] = dict(self.metadata)
        return data

    @property
    def rule_id(self) -> str | None:
        return dict(self.metadata).get('rule_id')


@dataclass(frozen=True)
class Profile:
    profile_id: str
    mode: Mode
    root: Node
    description: str = ''
    analysis_domains: tuple[tuple[str, DomainSpec], ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        data = {
            'profile_id': self.profile_id,
            'mode': self.mode,
            'description': self.description,
            'root': self.root.to_dict(),
        }
        if self.analysis_domains:
            data['analysis_domains'] = {k: v.to_dict() for k, v in self.analysis_domains}
        return data

    def domain_map(self) -> dict[str, DomainSpec]:
        return dict(self.analysis_domains)


ALLOWED_KEYS = {
    'TRUE': {'metadata'}, 'FALSE': {'metadata'}, 'AND': {'children', 'metadata'}, 'OR': {'children', 'metadata'}, 'NOT': {'children', 'metadata'},
    'EQ': {'path', 'value', 'metadata'}, 'NEQ': {'path', 'value', 'metadata'}, 'IN': {'path', 'value', 'metadata'}, 'NOT_IN': {'path', 'value', 'metadata'},
    'EXISTS': {'path', 'metadata'}, 'ABSENT': {'path', 'metadata'}, 'RANGE': {'path', 'low', 'high', 'metadata'}, 'MATCHES': {'path', 'value', 'metadata'},
    'AUTHORITY_EQ': {'path', 'value', 'metadata'}, 'TRUST_EQ': {'path', 'value', 'metadata'}, 'REGIME_EQ': {'path', 'value', 'metadata'}, 'EVIDENCE_EQ': {'path', 'value', 'metadata'}, 'ACTION_EQ': {'path', 'value', 'metadata'},
    'BEFORE_EQ': {'path', 'value', 'metadata'}, 'AFTER_EQ': {'path', 'value', 'metadata'}, 'BEFORE_RANGE': {'path', 'low', 'high', 'metadata'}, 'AFTER_RANGE': {'path', 'low', 'high', 'metadata'}, 'CHANGED': {'path', 'metadata'}, 'UNCHANGED': {'path', 'metadata'},
}


def _parse_domain_spec(data: dict[str, Any]) -> DomainSpec:
    if not isinstance(data, dict) or 'kind' not in data:
        raise StrictParseError('analysis domain must be an object with kind')
    kind = data['kind']
    if kind == 'enum':
        values = data.get('values')
        if not isinstance(values, list):
            raise StrictParseError('enum domain requires list values')
        return DomainSpec(kind='enum', values=tuple(values))
    if kind in {'bounded_int', 'bounded_decimal'}:
        if any(k not in data for k in ('min', 'max', 'step')):
            raise StrictParseError(f'{kind} domain requires min/max/step')
        return DomainSpec(kind=kind, min=data['min'], max=data['max'], step=data['step'])
    if kind == 'boolean':
        return DomainSpec(kind='boolean', values=(False, True))
    if kind == 'regex_witness':
        matching = data.get('matching', [])
        non_matching = data.get('non_matching', [])
        if not isinstance(matching, list) or not isinstance(non_matching, list):
            raise StrictParseError('regex_witness matching/non_matching must be lists')
        return DomainSpec(kind='regex_witness', matching=tuple(map(str, matching)), non_matching=tuple(map(str, non_matching)))
    raise StrictParseError(f'unsupported analysis domain kind: {kind}')


def parse_node(data: dict[str, Any]) -> Node:
    if not isinstance(data, dict):
        raise StrictParseError('constraint node must be an object')
    if 'kind' not in data:
        raise StrictParseError('constraint node missing kind')
    kind = data['kind']
    if kind not in ALLOWED_KEYS:
        raise StrictParseError(f'unsupported kind: {kind}')
    extras = set(data) - ({'kind'} | ALLOWED_KEYS[kind])
    if extras:
        raise StrictParseError(f'unknown keys for {kind}: {sorted(extras)}')
    children_data = data.get('children', [])
    if kind in {'AND', 'OR'} and not isinstance(children_data, list):
        raise StrictParseError(f'{kind}.children must be a list')
    if kind == 'NOT' and (not isinstance(children_data, list) or len(children_data) != 1):
        raise StrictParseError('NOT.children must contain exactly one child')
    metadata = data.get('metadata', {})
    if not isinstance(metadata, dict):
        raise StrictParseError('metadata must be an object')
    return Node(kind=kind, path=data.get('path'), value=data.get('value'), low=data.get('low'), high=data.get('high'), children=tuple(parse_node(c) for c in children_data), metadata=tuple(sorted(metadata.items())))


def parse_profile(data: dict[str, Any]) -> Profile:
    if not isinstance(data, dict):
        raise StrictParseError('profile must be an object')
    required = {'profile_id', 'mode', 'root'}
    extras = set(data) - (required | {'description', 'analysis_domains'})
    if extras:
        raise StrictParseError(f'unknown profile keys: {sorted(extras)}')
    missing = required - set(data)
    if missing:
        raise StrictParseError(f'missing profile keys: {sorted(missing)}')
    mode = data['mode']
    if mode not in {'object', 'transition'}:
        raise StrictParseError("mode must be 'object' or 'transition'")
    analysis_domains_data = data.get('analysis_domains', {})
    if not isinstance(analysis_domains_data, dict):
        raise StrictParseError('analysis_domains must be an object')
    analysis_domains = tuple(sorted((str(k), _parse_domain_spec(v)) for k, v in analysis_domains_data.items()))
    return Profile(profile_id=str(data['profile_id']), mode=mode, description=str(data.get('description', '')), root=parse_node(data['root']), analysis_domains=analysis_domains)


@dataclass(frozen=True)
class EvalContext:
    obj: dict[str, Any]
    authority: dict[str, Any]
    trust: dict[str, Any]
    regime: dict[str, Any]
    evidence: dict[str, Any]
    action: dict[str, Any]
    before: dict[str, Any]
    after: dict[str, Any]


def deep_get(data: dict[str, Any], path: str | None) -> Any:
    if path is None or path == '':
        return data
    cur: Any = data
    for part in path.split('.'):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def select_scope(node: Node, ctx: EvalContext) -> dict[str, Any]:
    if node.kind in {'EQ', 'NEQ', 'IN', 'NOT_IN', 'EXISTS', 'ABSENT', 'RANGE', 'MATCHES', 'AFTER_EQ', 'AFTER_RANGE'}:
        return ctx.obj
    if node.kind in {'BEFORE_EQ', 'BEFORE_RANGE', 'CHANGED', 'UNCHANGED'}:
        return ctx.before
    if node.kind == 'AUTHORITY_EQ':
        return ctx.authority
    if node.kind == 'TRUST_EQ':
        return ctx.trust
    if node.kind == 'REGIME_EQ':
        return ctx.regime
    if node.kind == 'EVIDENCE_EQ':
        return ctx.evidence
    if node.kind == 'ACTION_EQ':
        return ctx.action
    return {}


def atom_outcome(node: Node, ctx: EvalContext) -> tuple[bool, bool, Any]:
    scope = select_scope(node, ctx)
    value = deep_get(scope, node.path)
    if node.kind == 'TRUE':
        return True, False, value
    if node.kind == 'FALSE':
        return False, False, value
    if node.kind == 'EXISTS':
        return value is not None, False, value
    if node.kind == 'ABSENT':
        return value is None, False, value
    if node.kind in {'CHANGED', 'UNCHANGED'}:
        before = deep_get(ctx.before, node.path)
        after = deep_get(ctx.after, node.path)
        if before is None and after is None:
            return False, True, None
        changed = before != after
        return (changed if node.kind == 'CHANGED' else not changed), False, {'before': before, 'after': after}
    if value is None:
        return False, True, None
    if node.kind in {'EQ', 'AUTHORITY_EQ', 'TRUST_EQ', 'REGIME_EQ', 'EVIDENCE_EQ', 'ACTION_EQ', 'BEFORE_EQ', 'AFTER_EQ'}:
        return value == node.value, False, value
    if node.kind == 'NEQ':
        return value != node.value, False, value
    if node.kind == 'IN':
        return value in node.value, False, value
    if node.kind == 'NOT_IN':
        return value not in node.value, False, value
    if node.kind in {'RANGE', 'BEFORE_RANGE', 'AFTER_RANGE'}:
        try:
            return node.low <= value <= node.high, False, value
        except TypeError:
            return False, True, value
    if node.kind == 'MATCHES':
        import re
        try:
            return re.fullmatch(str(node.value), str(value)) is not None, False, value
        except re.error:
            return False, True, value
    return False, True, value


@dataclass(frozen=True)
class EvalResult:
    verdict: str
    matched: tuple[str, ...]
    failed: tuple[str, ...]
    fail_closed: bool = False
    decisive_rule_ids: tuple[str, ...] = ()


def atom_key(node: Node) -> str:
    parts = [node.kind]
    if node.path is not None:
        parts.append(node.path)
    if node.value is not None:
        parts.append(repr(node.value))
    if node.low is not None or node.high is not None:
        parts.append(f'[{repr(node.low)},{repr(node.high)}]')
    if node.rule_id:
        parts.append(f'rule={node.rule_id}')
    return ':'.join(parts)


def _decisive(node: Node) -> tuple[str, ...]:
    return (node.rule_id,) if node.rule_id else ()


def eval_node(node: Node, ctx: EvalContext) -> EvalResult:
    if node.kind in ALL_ATOMS:
        ok, fail_closed, _ = atom_outcome(node, ctx)
        key = atom_key(node)
        decisive = _decisive(node)
        return EvalResult(VERDICT_ALLOW if ok else VERDICT_DENY, (key,) if ok else (), () if ok else (key,), fail_closed, decisive)
    if node.kind == 'NOT':
        child = eval_node(node.children[0], ctx)
        return EvalResult(VERDICT_DENY if child.verdict == VERDICT_ALLOW else VERDICT_ALLOW, child.failed, child.matched, child.fail_closed, child.decisive_rule_ids)
    if node.kind == 'AND':
        matched: list[str] = []
        failed: list[str] = []
        decisive: list[str] = []
        fail_closed = False
        for child in node.children:
            result = eval_node(child, ctx)
            matched.extend(result.matched)
            failed.extend(result.failed)
            decisive.extend(result.decisive_rule_ids)
            fail_closed = fail_closed or result.fail_closed
            if result.verdict == VERDICT_DENY:
                return EvalResult(VERDICT_DENY, tuple(matched), tuple(failed), fail_closed, tuple(dict.fromkeys(decisive)))
        return EvalResult(VERDICT_ALLOW, tuple(matched), tuple(failed), fail_closed, tuple(dict.fromkeys(decisive)))
    if node.kind == 'OR':
        matched: list[str] = []
        failed: list[str] = []
        decisive: list[str] = []
        fail_closed = False
        for child in node.children:
            result = eval_node(child, ctx)
            matched.extend(result.matched)
            failed.extend(result.failed)
            decisive.extend(result.decisive_rule_ids)
            fail_closed = fail_closed or result.fail_closed
            if result.verdict == VERDICT_ALLOW:
                return EvalResult(VERDICT_ALLOW, tuple(matched), tuple(failed), fail_closed, tuple(dict.fromkeys(decisive)))
        return EvalResult(VERDICT_DENY, tuple(matched), tuple(failed), fail_closed, tuple(dict.fromkeys(decisive)))
    return EvalResult(VERDICT_DENY, (), (f'unsupported:{node.kind}',), True, ())


def evaluate_profile(profile: Profile, request: dict[str, Any]) -> EvalResult:
    obj = request.get('object', request) if profile.mode == 'object' else request.get('after', request.get('object', {}))
    ctx = EvalContext(obj=obj, authority=request.get('authority', {}), trust=request.get('trust', {}), regime=request.get('regime', {}), evidence=request.get('evidence', {}), action=request.get('action', {}), before=request.get('before', {}), after=request.get('after', obj))
    return eval_node(profile.root, ctx)


@dataclass(frozen=True)
class NormalizeResult:
    node: Node
    trace: tuple[str, ...]


def _sort_key(node: Node) -> tuple:
    return (node.kind, node.path or '', repr(node.value), repr(node.low), repr(node.high), tuple(_sort_key(c) for c in node.children))


def _is_negation_pair(a: Node, b: Node) -> bool:
    return a.kind == 'NOT' and a.children and _sort_key(a.children[0]) == _sort_key(b)


def normalize(node: Node) -> NormalizeResult:
    trace: list[str] = []

    def norm(n: Node) -> Node:
        if n.kind in ALL_ATOMS:
            return n
        if n.kind == 'NOT':
            child = norm(n.children[0])
            if child.kind == 'TRUE':
                trace.append('not-true->false')
                return Node('FALSE')
            if child.kind == 'FALSE':
                trace.append('not-false->true')
                return Node('TRUE')
            if child.kind == 'NOT':
                trace.append('double-negation')
                return child.children[0]
            return Node('NOT', children=(child,), metadata=n.metadata)
        if n.kind in {'AND', 'OR'}:
            flat: list[Node] = []
            for child in n.children:
                c = norm(child)
                if c.kind == n.kind:
                    trace.append(f'flatten-{n.kind.lower()}')
                    flat.extend(c.children)
                else:
                    flat.append(c)
            filtered: list[Node] = []
            seen: set[tuple] = set()
            for child in flat:
                if n.kind == 'AND' and child.kind == 'TRUE':
                    trace.append('and-drop-true')
                    continue
                if n.kind == 'OR' and child.kind == 'FALSE':
                    trace.append('or-drop-false')
                    continue
                if n.kind == 'AND' and child.kind == 'FALSE':
                    trace.append('and-short-false')
                    return Node('FALSE')
                if n.kind == 'OR' and child.kind == 'TRUE':
                    trace.append('or-short-true')
                    return Node('TRUE')
                key = _sort_key(child)
                if key in seen:
                    trace.append(f'dedupe-{n.kind.lower()}')
                    continue
                if any(_is_negation_pair(child, prev) or _is_negation_pair(prev, child) for prev in filtered):
                    trace.append(f'boolean-contradiction-{n.kind.lower()}')
                    return Node('FALSE') if n.kind == 'AND' else Node('TRUE')
                seen.add(key)
                filtered.append(child)
            filtered = sorted(filtered, key=_sort_key)
            if not filtered:
                trace.append(f'empty-{n.kind.lower()}-identity')
                return Node('TRUE') if n.kind == 'AND' else Node('FALSE')
            if len(filtered) == 1:
                trace.append(f'collapse-{n.kind.lower()}-singleton')
                return filtered[0]
            return Node(n.kind, children=tuple(filtered), metadata=n.metadata)
        return n

    out = norm(node)
    return NormalizeResult(node=out, trace=tuple(trace))


@dataclass(frozen=True)
class Witness:
    request: dict[str, Any]
    verdict_a: str
    verdict_b: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {'request': self.request, 'verdict_a': self.verdict_a, 'verdict_b': self.verdict_b}


@dataclass(frozen=True)
class SatisfiabilityResult:
    satisfiable: bool
    witness: Witness | None
    universe_size: int


@dataclass(frozen=True)
class ComparisonResult:
    relation: str
    witness_a_not_b: Witness | None = None
    witness_b_not_a: Witness | None = None
    universe_size: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            'relation': self.relation,
            'universe_size': self.universe_size,
            'witness_a_not_b': self.witness_a_not_b.to_dict() if self.witness_a_not_b else None,
            'witness_b_not_a': self.witness_b_not_a.to_dict() if self.witness_b_not_a else None,
        }


def expand_domain(spec: DomainSpec) -> tuple[Any, ...]:
    if spec.kind == 'enum':
        return spec.values
    if spec.kind == 'boolean':
        return (False, True)
    if spec.kind == 'bounded_int':
        cur = int(spec.min)
        out: list[int] = []
        while cur <= int(spec.max):
            out.append(cur)
            cur += int(spec.step)
        return tuple(out)
    if spec.kind == 'bounded_decimal':
        cur = float(spec.min)
        out: list[float] = []
        while cur <= float(spec.max) + 1e-9:
            out.append(round(cur, 12))
            cur += float(spec.step)
        return tuple(out)
    if spec.kind == 'regex_witness':
        return spec.matching + spec.non_matching
    return ()


def _insert(target: dict[str, Any], path: str, value: Any) -> None:
    parts = path.split('.')
    cur = target
    for part in parts[:-1]:
        cur = cur.setdefault(part, {})
    cur[parts[-1]] = value


def _scope_for_kind(kind: str) -> str:
    if kind in {'EQ', 'NEQ', 'IN', 'NOT_IN', 'RANGE', 'MATCHES', 'EXISTS', 'ABSENT'}:
        return 'object'
    if kind.startswith('AUTHORITY'):
        return 'authority'
    if kind.startswith('TRUST'):
        return 'trust'
    if kind.startswith('REGIME'):
        return 'regime'
    if kind.startswith('EVIDENCE'):
        return 'evidence'
    if kind.startswith('ACTION'):
        return 'action'
    if kind.startswith('BEFORE') or kind in {'CHANGED', 'UNCHANGED'}:
        return 'before'
    if kind.startswith('AFTER'):
        return 'after'
    return 'object'


def _qualified_path(kind: str, path: str) -> str:
    return f'{_scope_for_kind(kind)}.{path}'


def _collect_atoms(node: Node, bucket: dict[str, set[Any]]) -> None:
    if node.path:
        qpath = _qualified_path(node.kind, node.path)
        bucket.setdefault(qpath, set()).add(None)
        if node.kind in {'EQ', 'NEQ', 'AUTHORITY_EQ', 'TRUST_EQ', 'REGIME_EQ', 'EVIDENCE_EQ', 'ACTION_EQ', 'BEFORE_EQ', 'AFTER_EQ'}:
            bucket[qpath].add(node.value)
        elif node.kind in {'IN', 'NOT_IN'}:
            bucket[qpath].update(node.value)
            bucket[qpath].add('__outside__')
        elif node.kind in {'RANGE', 'BEFORE_RANGE', 'AFTER_RANGE'}:
            vals = [node.low, node.high]
            if isinstance(node.low, (int, float)) and isinstance(node.high, (int, float)):
                vals.extend([node.low - 1, node.high + 1, (node.low + node.high) / 2])
            bucket[qpath].update(vals)
        elif node.kind == 'MATCHES':
            bucket[qpath].update({str(node.value), 'mismatch'})
        elif node.kind == 'EXISTS':
            bucket[qpath].add('present')
        elif node.kind in {'CHANGED', 'UNCHANGED'}:
            bucket[qpath].update({'before-value', 'after-value'})
            bucket.setdefault(f'after.{node.path}', set()).update({None, 'after-value', 'before-value'})
    for child in node.children:
        _collect_atoms(child, bucket)


def _merge_profile_domains(bucket: dict[str, set[Any]], profile: Profile) -> None:
    for path, spec in profile.domain_map().items():
        bucket.setdefault(path, set()).update(expand_domain(spec))
        bucket.setdefault(path, set()).add(None)


def _bucket_to_scope_candidates(bucket: dict[str, set[Any]], scope: str) -> tuple[dict[str, Any], ...]:
    relevant = {path: values for path, values in bucket.items() if path.startswith(scope + '.')}
    if not relevant:
        return ({},)
    keys = sorted(relevant)
    values = [sorted(list(relevant[k]), key=repr) for k in keys]
    out: list[dict[str, Any]] = []
    for combo in product(*values):
        obj: dict[str, Any] = {}
        for full_path, value in zip(keys, combo, strict=True):
            path = full_path.split('.', 1)[1]
            if value is None:
                continue
            if value == 'present':
                _insert(obj, path, 'present')
            elif value == '__outside__':
                _insert(obj, path, '__outside__')
            else:
                _insert(obj, path, value)
        out.append(obj)
    return tuple(out)


def enumerate_requests(*profiles: Profile):
    bucket: dict[str, set[Any]] = {}
    for profile in profiles:
        _collect_atoms(profile.root, bucket)
        _merge_profile_domains(bucket, profile)
    after_candidates = _bucket_to_scope_candidates(bucket, 'after')
    object_candidates = _bucket_to_scope_candidates(bucket, 'object') or after_candidates
    authority_candidates = _bucket_to_scope_candidates(bucket, 'authority')
    trust_candidates = _bucket_to_scope_candidates(bucket, 'trust')
    regime_candidates = _bucket_to_scope_candidates(bucket, 'regime')
    evidence_candidates = _bucket_to_scope_candidates(bucket, 'evidence')
    action_candidates = _bucket_to_scope_candidates(bucket, 'action')
    before_candidates = _bucket_to_scope_candidates(bucket, 'before')
    after_candidates = after_candidates if after_candidates else object_candidates
    for obj, authority, trust, regime, evidence, action, before, after in product(object_candidates, authority_candidates, trust_candidates, regime_candidates, evidence_candidates, action_candidates, before_candidates, after_candidates):
        yield {'object': obj, 'authority': authority, 'trust': trust, 'regime': regime, 'evidence': evidence, 'action': action, 'before': before, 'after': after or obj}


def is_satisfiable(profile: Profile) -> SatisfiabilityResult:
    count = 0
    for request in enumerate_requests(profile):
        count += 1
        verdict = evaluate_profile(profile, request).verdict
        if verdict == VERDICT_ALLOW:
            return SatisfiabilityResult(True, Witness(request=request, verdict_a=verdict), count)
    return SatisfiabilityResult(False, None, count)


def compare_profiles(profile_a: Profile, profile_b: Profile) -> ComparisonResult:
    w_a_not_b = None
    w_b_not_a = None
    count = 0
    for request in enumerate_requests(profile_a, profile_b):
        count += 1
        a = evaluate_profile(profile_a, request).verdict
        b = evaluate_profile(profile_b, request).verdict
        if a == VERDICT_ALLOW and b == VERDICT_DENY and w_a_not_b is None:
            w_a_not_b = Witness(request=request, verdict_a=a, verdict_b=b)
        if b == VERDICT_ALLOW and a == VERDICT_DENY and w_b_not_a is None:
            w_b_not_a = Witness(request=request, verdict_a=a, verdict_b=b)
        if w_a_not_b and w_b_not_a:
            return ComparisonResult('INCOMPARABLE', w_a_not_b, w_b_not_a, count)
    if w_a_not_b and not w_b_not_a:
        return ComparisonResult('STRICTER_B', w_a_not_b, None, count)
    if w_b_not_a and not w_a_not_b:
        return ComparisonResult('STRICTER_A', None, w_b_not_a, count)
    return ComparisonResult('EQUIVALENT', None, None, count)


def minimize_profile(profile: Profile):
    from dataclasses import dataclass
    @dataclass(frozen=True)
    class MinimizeResult:
        root: Node
        removed_rules: tuple[str, ...]

    def semantic_key(node: Node) -> tuple:
        return (node.kind, node.path, repr(node.value), repr(node.low), repr(node.high), tuple(semantic_key(c) for c in node.children))

    original_children = profile.root.children if profile.root.kind == 'AND' else ()
    norm = normalize(profile.root).node
    removed: list[str] = []
    if original_children:
        seen: set[tuple] = set()
        for idx, child in enumerate(original_children):
            key = semantic_key(child)
            if key in seen:
                removed.append(child.rule_id or f'child_{idx}')
            seen.add(key)
    if norm.kind != 'AND':
        return MinimizeResult(norm, tuple(removed))
    current = list(norm.children)
    changed = True
    while changed:
        changed = False
        for idx, child in list(enumerate(current)):
            candidate_children = tuple(c for j, c in enumerate(current) if j != idx)
            if not candidate_children:
                continue
            candidate_root = candidate_children[0] if len(candidate_children) == 1 else Node('AND', children=candidate_children)
            candidate_profile = Profile(profile.profile_id, profile.mode, candidate_root, profile.description, profile.analysis_domains)
            full_profile = Profile(profile.profile_id, profile.mode, Node('AND', children=tuple(current)), profile.description, profile.analysis_domains)
            comp = compare_profiles(full_profile, candidate_profile)
            if comp.relation == 'EQUIVALENT':
                removed.append(child.rule_id or f'child_{idx}')
                current = list(candidate_children)
                changed = True
                break
    root = current[0] if len(current) == 1 else Node('AND', children=tuple(current))
    root = normalize(root).node
    return MinimizeResult(root=root, removed_rules=tuple(dict.fromkeys(removed)))


def extract_decisive_core(profile: Profile, request: dict[str, Any]) -> dict[str, Any]:
    norm = normalize(profile.root).node
    base = evaluate_profile(Profile(profile.profile_id, profile.mode, norm, profile.description, profile.analysis_domains), request)
    children = norm.children if norm.kind in {'AND', 'OR'} else (norm,)
    full_ids = tuple(c.rule_id or f'child_{i}' for i, c in enumerate(children))
    target = base.verdict
    chosen = children
    if len(children) > 1:
        for size in range(1, len(children) + 1):
            for subset in combinations(children, size):
                candidate_root = subset[0] if len(subset) == 1 else Node(norm.kind, children=tuple(subset))
                candidate_profile = Profile(profile.profile_id, profile.mode, candidate_root, profile.description, profile.analysis_domains)
                if evaluate_profile(candidate_profile, request).verdict == target:
                    chosen = tuple(subset)
                    break
            if chosen != children:
                break
    chosen_ids = tuple(c.rule_id or f'child_{i}' for i, c in enumerate(chosen))
    return {
        'verdict': target,
        'full_rule_ids': list(full_ids),
        'minimal_rule_ids': list(chosen_ids),
        'sufficient': True,
        'non_essential_rule_ids': [x for x in full_ids if x not in chosen_ids],
    }
