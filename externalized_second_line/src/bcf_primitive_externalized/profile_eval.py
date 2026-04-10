from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class EvalResult:
    verdict: str
    decisive_rule_ids: list[str]
    matched: list[str]
    failed: list[str]
    fail_closed: bool


def _metadata_rule_id(node: dict[str, Any]) -> str | None:
    metadata = node.get('metadata')
    if isinstance(metadata, dict):
        rid = metadata.get('rule_id')
        return rid if isinstance(rid, str) else None
    return None


def _get_value(obj: dict[str, Any], path: str | None) -> Any:
    if path is None:
        return None
    cur: Any = obj
    for part in path.split('.'):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _eval_node(node: dict[str, Any], obj: dict[str, Any], matched: list[str], failed: list[str]) -> bool:
    kind = node['kind']
    rid = _metadata_rule_id(node)
    if kind == 'AND':
        ok = all(_eval_node(child, obj, matched, failed) for child in node.get('children', []))
    elif kind == 'OR':
        ok = any(_eval_node(child, obj, matched, failed) for child in node.get('children', []))
    elif kind == 'NOT':
        children = node.get('children', [])
        ok = len(children) == 1 and (not _eval_node(children[0], obj, matched, failed))
    elif kind == 'EQ':
        ok = _get_value(obj, node.get('path')) == node.get('value')
    elif kind == 'NEQ':
        ok = _get_value(obj, node.get('path')) != node.get('value')
    elif kind == 'IN':
        ok = _get_value(obj, node.get('path')) in list(node.get('value', []))
    elif kind == 'NOT_IN':
        ok = _get_value(obj, node.get('path')) not in list(node.get('value', []))
    elif kind == 'RANGE':
        value = _get_value(obj, node.get('path'))
        ok = isinstance(value, (int, float)) and value >= node.get('low') and value <= node.get('high')
    elif kind == 'EXISTS':
        ok = _get_value(obj, node.get('path')) is not None
    elif kind == 'ABSENT':
        ok = _get_value(obj, node.get('path')) is None
    else:
        raise ValueError(f'unsupported node kind: {kind}')
    if rid:
        (matched if ok else failed).append(rid)
    return ok


def evaluate_request(profile: dict[str, Any], request: dict[str, Any]) -> EvalResult:
    if not isinstance(request, dict):
        return EvalResult('DENY', [], [], ['request_not_object'], True)
    obj = request.get('object')
    if not isinstance(obj, dict):
        return EvalResult('DENY', [], [], ['object_missing'], True)
    matched: list[str] = []
    failed: list[str] = []
    root = profile['root']
    ok = _eval_node(root, obj, matched, failed)
    decisive = list(matched if ok else failed)
    return EvalResult('ALLOW' if ok else 'DENY', decisive, matched, failed, False)
