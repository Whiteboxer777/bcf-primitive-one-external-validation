# BCF Primitive One — Expected External Truth Closure Outputs

These are the reference values from the internal canonical run. An independent external rerun on the
same commit MUST produce identical source-file digests (artifact_digest may differ if dist/ state
changes, but all source-bound digests must match).

## Reference Verdict (from internal canonical run)

```
verdict: EXTERNAL_TRUTH_CLOSED_INTERNAL_CLEAN_ROOM
overall_ok: true
artifact_id: BCF_PRIMITIVE_ONE_EXTERNAL_TRUTH_CLOSURE
```

## Reference Source-File Digests (MUST MATCH exactly on rerun)

| Artifact | SHA-256 |
|----------|---------|
| `src/bcf_trust_kernel/__init__.py` | `1152b8f21fea8404be01409ff2e90cb85cbf75b85cf1054768d433db6b6679b2` |
| `src/bcf_primitive_verifier/verifier.py` | `684b48c9faf21d3ff99c39bb35d3e22ef91b8824c42fbdd7da930eedf4b963e2` |
| `src/bcf_primitive/runtime.py` | `573a82fc30fc1ea0cb8d6468fe42044ac5e7304286a1c7a76628c6c1d239af31` |
| `src/bcf_primitive_independent/semantic_core.py` | `08db2fea157406ab1b2c475d2f0dc8284b6fd3b82d9159c6b43b52046bc21949` |
| `node_second_line/src/runtime.mjs` | `87565c8726e9b4e70ea8cbc2bb7e4160cb2ac1039daa286e09eb39c62bea0273` |
| `bundle_digest` | `35fa718e57fb5bda7693fdfdaf474477f41caecba84d9b24d2ca08454c59ec06` |

## Reference Parity Outcomes (MUST ALL BE TRUE)

### Independent Python (4 cases)
- `allow_replay`: true
- `allow_runtime`: true
- `deny_replay`: true
- `deny_runtime`: true
- `verify`: true

### Node Out-of-Family (4 cases)
- `allow_replay`: true
- `allow_runtime`: true
- `deny_replay`: true
- `deny_runtime`: true
- `verify`: true

## Verification Script

```python
import json, sys

verdict = json.loads(open("dist/EXTERNAL_TRUTH_VERDICT.json").read())

EXPECTED_SOURCE_DIGESTS = {
    "trust_kernel_digests.bcf_trust_kernel_init":
        "1152b8f21fea8404be01409ff2e90cb85cbf75b85cf1054768d433db6b6679b2",
    "verifier_digest_set.bcf_primitive_verifier_verifier":
        "684b48c9faf21d3ff99c39bb35d3e22ef91b8824c42fbdd7da930eedf4b963e2",
    "runtime_digest_set.bcf_primitive_runtime":
        "573a82fc30fc1ea0cb8d6468fe42044ac5e7304286a1c7a76628c6c1d239af31",
    "independent_line_digest_set.bcf_primitive_independent_semantic_core":
        "08db2fea157406ab1b2c475d2f0dc8284b6fd3b82d9159c6b43b52046bc21949",
    "node_line_digest_set.node_second_line_runtime":
        "87565c8726e9b4e70ea8cbc2bb7e4160cb2ac1039daa286e09eb39c62bea0273",
}

failures = []
if not verdict.get("overall_ok"):
    failures.append("overall_ok is not true")
if verdict.get("verdict") != "EXTERNAL_TRUTH_CLOSED_INTERNAL_CLEAN_ROOM":
    failures.append(f"unexpected verdict: {verdict.get('verdict')}")

for key, expected in EXPECTED_SOURCE_DIGESTS.items():
    section, field = key.split(".", 1)
    actual = verdict.get(section, {}).get(field)
    if actual != expected:
        failures.append(f"digest mismatch: {key} = {actual!r} (expected {expected!r})")

if failures:
    for f in failures:
        print("FAIL:", f)
    sys.exit(1)
print("ALL CHECKS PASS")
```
