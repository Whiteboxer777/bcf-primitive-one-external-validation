from __future__ import annotations
import argparse, json
from .runtime import replay_verdict
from .strict_json import load_path_strict
from .verifier import verify_bundle


def main() -> None:
    parser = argparse.ArgumentParser(prog='bcf-standalone-verifier-primitive')
    sub = parser.add_subparsers(dest='cmd', required=True)

    p_verify = sub.add_parser('verify-bundle')
    p_verify.add_argument('bundle')

    p_replay = sub.add_parser('replay-verdict')
    p_replay.add_argument('bundle')
    p_replay.add_argument('request')

    p_audit = sub.add_parser('audit-bundle')
    p_audit.add_argument('bundle')
    p_audit.add_argument('--allow-request')
    p_audit.add_argument('--deny-request')

    args = parser.parse_args()
    if args.cmd == 'verify-bundle':
        print(json.dumps(verify_bundle(args.bundle), indent=2, sort_keys=True))
        return
    if args.cmd == 'replay-verdict':
        print(json.dumps(replay_verdict(args.bundle, load_path_strict(args.request)), indent=2, sort_keys=True))
        return
    verify_report = verify_bundle(args.bundle)
    payload = {'verify_report': verify_report, 'overall_ok': bool(verify_report.get('overall_ok'))}
    if args.allow_request:
        payload['allow_replay'] = replay_verdict(args.bundle, load_path_strict(args.allow_request))
        payload['overall_ok'] = payload['overall_ok'] and bool(payload['allow_replay'].get('overall_ok')) and payload['allow_replay'].get('verdict') == 'ALLOW'
    if args.deny_request:
        payload['deny_replay'] = replay_verdict(args.bundle, load_path_strict(args.deny_request))
        payload['overall_ok'] = payload['overall_ok'] and bool(payload['deny_replay'].get('overall_ok')) and payload['deny_replay'].get('verdict') == 'DENY'
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
