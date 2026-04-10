from __future__ import annotations

from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import json, shutil, tempfile
from bcf_primitive.compiler import compile_bundle
from bcf_primitive.runtime import SealedBoundaryRunner, refuse_non_bypass
from bcf_primitive.strict_json import load_path_strict
from bcf_primitive_verifier.runtime import replay_verdict
from bcf_primitive_verifier.verifier import verify_bundle

def run_external_audit(profile: str | Path, allow_request: str | Path, deny_request: str | Path) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="bcf_primitive_audit_") as td:
        bundle = Path(td) / "bundle"
        compile_report = compile_bundle(profile, bundle)
        verify_report = verify_bundle(bundle)
        allow_req = load_path_strict(allow_request)
        deny_req = load_path_strict(deny_request)
        replay_allow = replay_verdict(bundle, allow_req)
        replay_deny = replay_verdict(bundle, deny_req)
        runner = SealedBoundaryRunner(bundle)
        sealed_allow = runner.execute(allow_req, {"action_id": "allow", "kind": "emit", "payload": {"stage": "prod"}})
        sealed_deny = runner.execute(deny_req, {"action_id": "deny", "kind": "emit", "payload": {"stage": "prod"}})
        tampered = Path(td) / "tampered"
        shutil.copytree(bundle, tampered)
        (tampered / "CLAIM.json").write_text('{"tampered": true}', encoding="utf-8")
        tamper_verify = verify_bundle(tampered)
        missing = Path(td) / "missing"
        shutil.copytree(bundle, missing)
        (missing / "TRUST_ROOTS.json").unlink()
        missing_verify = verify_bundle(missing)
        oversized_refusal = None
        try:
            runner.execute({"blob": "x" * (70 * 1024)}, {"action_id": "oversized", "kind": "emit", "payload": {}})
        except RuntimeError as exc:
            oversized_refusal = str(exc)
        non_bypass = refuse_non_bypass(bundle, allow_req, "direct-runtime-eval")
        overall_ok = bool(
            compile_report["overall_ok"]
            and verify_report["overall_ok"]
            and replay_allow["overall_ok"]
            and replay_allow["verdict"] == "ALLOW"
            and replay_deny["verdict"] == "REFUSAL" and replay_deny["refusal_code"] == "REFUSE_VERDICT_NOT_ALLOW"
            and sealed_allow["permit"] is True
            and sealed_deny["permit"] is False
            and "REFUSE_CLAIM_TCB_INVALID" in tamper_verify.get("refusal_reasons", [])
            and "REFUSE_REQUIRED_FILES_MISSING" in missing_verify.get("refusal_reasons", [])
            and non_bypass["refusal_code"] == "REFUSE_NON_BYPASS_VIOLATION"
            and oversized_refusal == "runtime_refusal:request_too_large"
        )
        return {
            "overall_ok": overall_ok,
            "compile_report": compile_report,
            "verify_report": verify_report,
            "replay_allow": replay_allow,
            "replay_deny": replay_deny,
            "sealed_allow": sealed_allow,
            "sealed_deny": sealed_deny,
            "tamper_verify": tamper_verify,
            "missing_verify": missing_verify,
            "non_bypass_refusal": non_bypass,
            "oversized_refusal": oversized_refusal,
        }

if __name__ == "__main__":
    print(json.dumps(run_external_audit(sys.argv[1], sys.argv[2], sys.argv[3]), indent=2, sort_keys=True))
