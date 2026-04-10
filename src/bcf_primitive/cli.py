from __future__ import annotations
import argparse, json
from pathlib import Path
from .capsule import build_standalone_verifier_release
from .compiler import compile_bundle
from .proof import run_one_shot_proof
from .runtime import SealedBoundaryRunner
from .strict_json import load_path_strict
from .verifier import verify_bundle
def main() -> None:
    parser = argparse.ArgumentParser(prog='bcf-primitive'); sub = parser.add_subparsers(dest='cmd', required=True)
    p_compile = sub.add_parser('compile'); p_compile.add_argument('profile'); p_compile.add_argument('--out', required=True)
    p_verify = sub.add_parser('verify-bundle'); p_verify.add_argument('bundle')
    p_run = sub.add_parser('sealed-run'); p_run.add_argument('bundle'); p_run.add_argument('request'); p_run.add_argument('action_descriptor')
    p_prove = sub.add_parser('prove'); p_prove.add_argument('--profile', required=True); p_prove.add_argument('--allow-request', required=True); p_prove.add_argument('--deny-request', required=True)
    p_caps = sub.add_parser('build-standalone-verifier'); p_caps.add_argument('--project-root', default=str(Path(__file__).resolve().parents[2])); p_caps.add_argument('--out', required=True)
    args = parser.parse_args()
    if args.cmd == 'compile': print(json.dumps(compile_bundle(args.profile, args.out), indent=2, sort_keys=True))
    elif args.cmd == 'verify-bundle': print(json.dumps(verify_bundle(args.bundle), indent=2, sort_keys=True))
    elif args.cmd == 'sealed-run': print(json.dumps(SealedBoundaryRunner(args.bundle).execute(load_path_strict(args.request), load_path_strict(args.action_descriptor)), indent=2, sort_keys=True))
    elif args.cmd == 'prove': print(json.dumps(run_one_shot_proof(args.profile, args.allow_request, args.deny_request), indent=2, sort_keys=True))
    elif args.cmd == 'build-standalone-verifier': print(json.dumps(build_standalone_verifier_release(args.project_root, args.out), indent=2, sort_keys=True))
if __name__ == '__main__': main()
