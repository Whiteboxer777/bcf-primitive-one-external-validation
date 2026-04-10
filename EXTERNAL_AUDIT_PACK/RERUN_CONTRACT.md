# BCF Primitive One — External Rerun Contract

## Who This Is For

Any second-party or external auditor who wants to independently verify that BCF Primitive One
produces the same external truth closure on a fresh machine and environment.

## What You Need

- Git (to clone this repo)
- Python 3.11+ (`python3 --version`)
- Node.js 18+ (optional but recommended; gate falls back to pre-generated dist/ cache if absent)
- No build system, no Docker, no special toolchain

## How to Rerun

```bash
# 1. Clone (or use the provided ZIP)
git clone <this-repo> bcf-primitive-one-external
cd bcf-primitive-one-external

# 2. Install Python deps
pip install -r requirements.txt

# 3. Run the external truth closure gate
PYTHONPATH=src PYTHONDONTWRITEBYTECODE=1 python tools/external_truth_closure_gate.py

# 4. Check the verdict
python - <<'EOF'
import json, sys
v = json.loads(open("dist/EXTERNAL_TRUTH_VERDICT.json").read())
assert v["overall_ok"] is True, f"FAIL: {v}"
assert v["verdict"] == "EXTERNAL_TRUTH_CLOSED_INTERNAL_CLEAN_ROOM", f"FAIL: {v['verdict']}"
print("PASS:", v["verdict"])
EOF
```

## What Must Hold

1. `dist/EXTERNAL_TRUTH_VERDICT.json` must exist and have `overall_ok: true`
2. `verdict` field must be `"EXTERNAL_TRUTH_CLOSED_INTERNAL_CLEAN_ROOM"`
3. All source-file digests (trust kernel, verifier, runtime, independent line, node line) must match
   the reference values in `EXTERNAL_AUDIT_PACK/EXPECTED_OUTPUTS.md`
4. All parity outcomes must be `true`
5. CI must not exit 0 unless the above hold

## What Is NOT Required for This Contract

- Running the full internal test suite (`pytest tests/`) — that is for internal development
- Having mechanized kernel tools installed (Lean, Coq) — those are used only for PROOFS/
- Access to internal HISTORY/ or REPORTS/ — those are development artifacts

## Residual Gaps (Acknowledged)

- **RG-04**: External hosted CI attestation has not yet been triggered by an independent party on
  a separate hosted CI account. The CI template in `.github/workflows/` is ready for this.
- **RG-05**: Whole-family theorem-prover complete closure is scoped to the mechanized kernel;
  full formal discharge is acknowledged as out-of-scope for this release.

## Minimum Acceptable Attestation

An external party who runs this gate and finds `overall_ok: true` with matching source digests
has produced an independent attestation that:

- The BCF trust kernel, verifier, runtime, independent line, and node line are the same hard objects
- The compiled bundle is deterministically produced and verifies
- All four parity cases agree across primary Python, independent Python, and Node.js
- No forbidden artifacts are present in the release surface
- The external truth chain is self-consistent
