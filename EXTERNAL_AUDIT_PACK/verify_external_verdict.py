#!/usr/bin/env python3
"""
Verify that dist/EXTERNAL_TRUTH_VERDICT.json matches the reference source-file digests.
Run this after external_truth_closure_gate.py completes.

Usage:
    python EXTERNAL_AUDIT_PACK/verify_external_verdict.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERDICT_PATH = ROOT / "dist" / "EXTERNAL_TRUTH_VERDICT.json"

# Reference source-file digests (authoritative — must not change between reruns)
EXPECTED_SOURCE_DIGESTS = {
    ("trust_kernel_digests", "bcf_trust_kernel_init"):
        "1152b8f21fea8404be01409ff2e90cb85cbf75b85cf1054768d433db6b6679b2",
    ("verifier_digest_set", "bcf_primitive_verifier_verifier"):
        "684b48c9faf21d3ff99c39bb35d3e22ef91b8824c42fbdd7da930eedf4b963e2",
    ("runtime_digest_set", "bcf_primitive_runtime"):
        "573a82fc30fc1ea0cb8d6468fe42044ac5e7304286a1c7a76628c6c1d239af31",
    ("independent_line_digest_set", "bcf_primitive_independent_semantic_core"):
        "08db2fea157406ab1b2c475d2f0dc8284b6fd3b82d9159c6b43b52046bc21949",
    ("node_line_digest_set", "node_second_line_runtime"):
        "87565c8726e9b4e70ea8cbc2bb7e4160cb2ac1039daa286e09eb39c62bea0273",
}

EXPECTED_BUNDLE_DIGEST = "35fa718e57fb5bda7693fdfdaf474477f41caecba84d9b24d2ca08454c59ec06"


def main() -> int:
    if not VERDICT_PATH.exists():
        print("FAIL: dist/EXTERNAL_TRUTH_VERDICT.json not found — run external_truth_closure_gate.py first")
        return 1

    verdict = json.loads(VERDICT_PATH.read_text(encoding="utf-8"))
    failures: list[str] = []

    # Top-level checks
    if not verdict.get("overall_ok"):
        failures.append(f"overall_ok is {verdict.get('overall_ok')!r} — expected true")
    if verdict.get("verdict") != "EXTERNAL_TRUTH_CLOSED_INTERNAL_CLEAN_ROOM":
        failures.append(f"verdict = {verdict.get('verdict')!r} — expected 'EXTERNAL_TRUTH_CLOSED_INTERNAL_CLEAN_ROOM'")
    if verdict.get("artifact_id") != "BCF_PRIMITIVE_ONE_EXTERNAL_TRUTH_CLOSURE":
        failures.append(f"artifact_id = {verdict.get('artifact_id')!r}")

    # Source-file digest checks
    for (section, field), expected in EXPECTED_SOURCE_DIGESTS.items():
        actual = verdict.get(section, {}).get(field)
        if actual != expected:
            failures.append(f"digest mismatch: {section}.{field}\n  got:      {actual!r}\n  expected: {expected!r}")

    # Bundle digest
    actual_bundle = verdict.get("bundle_digest")
    if actual_bundle != EXPECTED_BUNDLE_DIGEST:
        failures.append(f"bundle_digest mismatch:\n  got:      {actual_bundle!r}\n  expected: {EXPECTED_BUNDLE_DIGEST!r}")

    # Parity outcomes
    parity = verdict.get("parity_outcomes", {})
    if not parity.get("independent_overall"):
        failures.append("parity_outcomes.independent_overall is not true")
    if not parity.get("node_overall"):
        failures.append("parity_outcomes.node_overall is not true")
    for case, ok in parity.get("independent_python", {}).items():
        if not ok:
            failures.append(f"parity_outcomes.independent_python.{case} = {ok!r}")
    for case, ok in parity.get("node_out_of_family", {}).items():
        if not ok:
            failures.append(f"parity_outcomes.node_out_of_family.{case} = {ok!r}")

    # Sub-outcomes
    if not verdict.get("proof_outcome", {}).get("proof_ok"):
        failures.append("proof_outcome.proof_ok is not true")
    if not verdict.get("audit_outcome", {}).get("overall_ok"):
        failures.append("audit_outcome.overall_ok is not true")
    if not verdict.get("hygiene_outcome", {}).get("overall_ok"):
        failures.append("hygiene_outcome.overall_ok is not true")
    if not verdict.get("digest_reconciliation_outcome"):
        failures.append("digest_reconciliation_outcome is not true")

    # Gap closure checks
    if not verdict.get("theorem_discharge_outcome", {}).get("overall_ok"):
        failures.append("theorem_discharge_outcome.overall_ok is not true (RG-05)")
    if not verdict.get("ci_simulation_outcome", {}).get("overall_ok"):
        failures.append("ci_simulation_outcome.overall_ok is not true (RG-04)")
    if verdict.get("residual_gaps"):
        failures.append(f"residual_gaps not empty: {verdict['residual_gaps']}")

    if failures:
        print(f"EXTERNAL TRUTH VERIFICATION FAILED ({len(failures)} issue(s)):")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("EXTERNAL TRUTH VERIFICATION PASSED")
    print(f"  verdict:           {verdict['verdict']}")
    print(f"  artifact_id:       {verdict['artifact_id']}")
    print(f"  bundle:            {verdict['bundle_digest']}")
    print(f"  residual_gaps:     {verdict.get('residual_gaps', [])}")
    print(f"  closed_gaps:       {len(verdict.get('closed_gaps', []))}")
    print(f"  theorem_discharge: {verdict.get('theorem_discharge_outcome', {}).get('discharge_grade')}")
    print(f"  ci_simulation:     {verdict.get('ci_simulation_outcome', {}).get('simulation_grade')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
