from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from jsonschema import Draft202012Validator
from bcf_primitive.compiler import compile_bundle
from bcf_primitive.runtime import SealedBoundaryRunner
from bcf_primitive_verifier.runtime import replay_verdict
from bcf_primitive_verifier.verifier import verify_bundle
from bcf_primitive_verifier.refusal import REFUSAL_SCHEMA, PERMIT_SCHEMA, VERIFICATION_RESULT_SCHEMA


def _validate(schema: dict[str, object], payload: dict[str, object]) -> dict[str, object]:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.path))
    return {
        'ok': not errors,
        'error_count': len(errors),
        'errors': [
            {
                'path': list(error.path),
                'message': error.message,
            }
            for error in errors
        ],
    }


def run_schema_validation_harness(project_root: str | Path, profile: str | Path) -> dict[str, object]:
    project_root = Path(project_root)
    profile = Path(profile)
    bundle = project_root / '.schema_validation_bundle_tmp'
    if bundle.exists():
        import shutil
        shutil.rmtree(bundle)
    compile_bundle(profile, bundle)
    runner = SealedBoundaryRunner(bundle)
    allow_request = {'object': {'vendor': 'ACME', 'currency': 'EUR', 'amount': 5000}}
    deny_request = {'object': {'vendor': 'ACME', 'currency': 'EUR', 'amount': 11000}}

    verification = verify_bundle(bundle)
    permit = runner.execute(allow_request, {'action_id': 'schema-allow', 'kind': 'emit', 'payload': {}})
    refusal = runner.execute(deny_request, {'action_id': 'schema-deny', 'kind': 'emit', 'payload': {}})
    broken_bundle = project_root / '.schema_validation_broken_bundle_tmp'
    if broken_bundle.exists():
        import shutil
        shutil.rmtree(broken_bundle)
    compile_bundle(profile, broken_bundle)
    (broken_bundle / 'TRUST_ROOTS.json').unlink()
    replay_refusal = replay_verdict(broken_bundle, allow_request)

    report = {
        'verification': {
            'payload': verification,
            'schema_validation': _validate(VERIFICATION_RESULT_SCHEMA, verification),
        },
        'permit': {
            'payload': permit,
            'schema_validation': _validate(PERMIT_SCHEMA, permit),
        },
        'refusal': {
            'payload': refusal,
            'schema_validation': _validate(REFUSAL_SCHEMA, refusal),
        },
        'replay_refusal': {
            'payload': replay_refusal,
            'schema_validation': _validate(REFUSAL_SCHEMA, replay_refusal),
        },
    }
    report['overall_ok'] = all(entry['schema_validation']['ok'] for entry in report.values())

    import shutil
    shutil.rmtree(bundle)
    shutil.rmtree(broken_bundle)
    return report


if __name__ == '__main__':
    print(json.dumps(run_schema_validation_harness(ROOT, ROOT / 'examples' / 'canonical' / 'invoice_profile.json'), indent=2, sort_keys=True))
