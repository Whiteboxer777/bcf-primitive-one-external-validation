
export function evaluateRequest(profile, request) {
  if (!request || typeof request !== 'object' || Array.isArray(request)) {
    return { verdict: 'DENY', decisive_rule_ids: [], matched: [], failed: ['request_not_object'], fail_closed: true };
  }
  const obj = profile.mode === 'object' ? (request.object || request) : (request.after || (request.object || {}));
  if (!obj || typeof obj !== 'object' || Array.isArray(obj)) {
    return { verdict: 'DENY', decisive_rule_ids: [], matched: [], failed: ['object_missing'], fail_closed: true };
  }
  const matched = [];
  const failed = [];
  function metadataRuleId(node) {
    return node && node.metadata && typeof node.metadata.rule_id === 'string' ? node.metadata.rule_id : null;
  }
  function deepGet(data, p) {
    if (!p) return null;
    let cur = data;
    for (const part of p.split('.')) {
      if (!cur || typeof cur !== 'object' || Array.isArray(cur) || !(part in cur)) return null;
      cur = cur[part];
    }
    return cur;
  }
  function evalNode(node) {
    const kind = node.kind;
    const rid = metadataRuleId(node);
    let ok = false;
    if (kind === 'AND') ok = (node.children || []).every(evalNode);
    else if (kind === 'OR') ok = (node.children || []).some(evalNode);
    else if (kind === 'NOT') {
      const ch = node.children || [];
      ok = ch.length === 1 && !evalNode(ch[0]);
    } else if (kind === 'EQ') ok = deepGet(obj, node.path) === node.value;
    else if (kind === 'NEQ') ok = deepGet(obj, node.path) !== node.value;
    else if (kind === 'IN') ok = Array.isArray(node.value) && node.value.includes(deepGet(obj, node.path));
    else if (kind === 'NOT_IN') ok = Array.isArray(node.value) && !node.value.includes(deepGet(obj, node.path));
    else if (kind === 'RANGE') {
      const v = deepGet(obj, node.path);
      ok = typeof v === 'number' && v >= node.low && v <= node.high;
    } else if (kind === 'EXISTS') ok = deepGet(obj, node.path) !== null;
    else if (kind === 'ABSENT') ok = deepGet(obj, node.path) === null;
    else throw new Error(`unsupported node kind: ${kind}`);
    if (rid) (ok ? matched : failed).push(rid);
    return ok;
  }
  const ok = evalNode(profile.root);
  const decisive_rule_ids = ok ? [...matched] : [...failed];
  return { verdict: ok ? 'ALLOW' : 'DENY', decisive_rule_ids, matched, failed, fail_closed: false };
}
