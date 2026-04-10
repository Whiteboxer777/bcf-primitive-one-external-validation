#!/usr/bin/env python3
"""
Whole-family theorem discharge gate — closes RG-05.

Combines:
  1. Full mechanized kernel discharge (K1-K14 over 4096 abstract states + concrete tests)
  2. All existing gate reports verified
  3. Refusal/permit algebra concrete execution tests
  4. Witness-certificate chain integrity across all execution paths
  5. Corpus-wide theorem family coverage

Produces: dist/whole_family_theorem_discharge_report.json
"""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mechanized_kernel.full_family_discharge import run_full_family_discharge
from bcf_primitive.compiler import compile_bundle
from bcf_primitive.runtime import SealedBoundaryRunner, refuse_non_bypass
from bcf_primitive.common import load_json
from bcf_primitive_verifier.verifier import verify_bundle
from bcf_primitive_verifier.runtime import replay_verdict
from bcf_primitive_verifier.witness_certificate import WITNESS_CERTIFICATE_SCHEMA, strip_witness_certificate
from jsonschema import Draft202012Validator

EXAMPLES = ROOT / 'examples' / 'canonical'
OUT_D = ROOT / 'dist' / 'whole_family_theorem_discharge_report.json'
OUT_R = ROOT / 'REPORTS' / 'whole_family_theorem_discharge_report.json'


def _validate_witness(payload: dict[str, object]) -> dict[str, object]:
    cert = payload.get('witness_certificate')
    if not isinstance(cert, dict):
        return {'ok': False, 'reason': 'missing_witness_certificate'}
    validator = Draft202012Validator(WITNESS_CERTIFICATE_SCHEMA)
    errs = list(validator.iter_errors(cert))
    source = strip_witness_certificate(payload)
    from bcf_primitive_verifier.common import digest_data
    body = {k: v for k, v in cert.items() if k != 'certificate_digest'}
    return {
        'ok': not errs and cert.get('source_digest') == digest_data(source) and cert.get('certificate_digest') == digest_data(body),
        'schema_ok': not errs,
        'source_digest_ok': cert.get('source_digest') == digest_data(source),
        'certificate_digest_ok': cert.get('certificate_digest') == digest_data(body),
        'certificate_type': cert.get('certificate_type'),
    }


def _load_gate_report(name: str) -> dict[str, Any]:
    path = ROOT / 'dist' / f'{name}.json'
    if not path.exists():
        return {'overall_ok': False, 'error': f'report_not_found: {name}'}
    return json.loads(path.read_text(encoding='utf-8'))


def _verify_all_existing_gates() -> dict[str, Any]:
    """Check that all required gate reports exist and passed."""
    required = [
        'mechanized_kernel_gate_report',
        'admission_normal_form_gate_report',
        'compiled_backend_gate_report',
        'witness_certificate_gate_report',
        'whole_family_mechanization_expansion_report',
        'schema_validation_report',
        'equivalence_report',
        'theorem_family_corpus_report',
        'adversarial_closure_report',
        'verification_subfamily_completion_report',
        'independent_second_implementation_parity_report',
        'object_canonicalization_impossibility_saturation_report',
    ]
    optional = [
        'node_out_of_family_parity_report',
        'node_verification_subfamily_parity_report',
        'witness_certificate_expansion_report',
    ]
    results = {}
    all_required_ok = True
    for name in required:
        r = _load_gate_report(name)
        ok = r.get('overall_ok', False)
        results[name] = {'ok': ok}
        if not ok:
            all_required_ok = False
    for name in optional:
        r = _load_gate_report(name)
        ok = r.get('overall_ok', False)
        results[name] = {'ok': ok, 'optional': True}
    return {'ok': all_required_ok, 'reports': results}


def _refusal_permit_algebra_test() -> dict[str, Any]:
    """Verify refusal/permit algebra on real bundle execution paths."""
    with tempfile.TemporaryDirectory(prefix='rpa_') as td:
        bundle = Path(td) / 'bundle'
        compile_bundle(EXAMPLES / 'invoice_profile.json', bundle)
        runner = SealedBoundaryRunner(bundle)
        action = {'action_id': 'rpa-test', 'kind': 'emit', 'payload': {}}

        allow_req = load_json(EXAMPLES / 'invoice_request_allow.json')
        deny_req = load_json(EXAMPLES / 'invoice_deny_request.json')

        permit = runner.execute(allow_req, action)
        refusal = runner.execute(deny_req, action)
        replay_allow = replay_verdict(bundle, allow_req)
        replay_deny = replay_verdict(bundle, deny_req)
        no_bypass = refuse_non_bypass(bundle, allow_req, 'discharge-gate-direct')

        # Permit algebra checks
        permit_checks = {
            'verdict_is_allow': permit.get('verdict') == 'ALLOW',
            'has_primitive_identity': 'primitive_identity' in permit,
            'has_bundle_digest': 'bundle_digest' in permit,
            'has_request_digest': 'request_digest' in permit,
            'has_action_digest': 'action_digest' in permit,
            'has_witness_certificate': 'witness_certificate' in permit,
            'witness_valid': _validate_witness(permit)['ok'],
        }

        # Refusal algebra checks
        refusal_details = refusal.get('details', {})
        refusal_checks = {
            'verdict_is_refusal': refusal.get('verdict') == 'REFUSAL',
            'has_refusal_code': 'refusal_code' in refusal,
            'has_refusal_class': 'refusal_class' in refusal,
            'has_decisive_rule_ids': 'decisive_rule_ids' in (refusal_details if isinstance(refusal_details, dict) else {}),
            'has_witness_certificate': 'witness_certificate' in refusal,
            'witness_valid': _validate_witness(refusal)['ok'],
        }

        # Replay determinism
        replay_checks = {
            'replay_allow_matches': replay_allow.get('verdict') == permit.get('verdict'),
            'replay_deny_matches': replay_deny.get('verdict') == refusal.get('verdict'),
            'replay_allow_witness_valid': _validate_witness(replay_allow)['ok'],
            'replay_deny_witness_valid': _validate_witness(replay_deny)['ok'],
        }

        # No-bypass enforcement
        no_bypass_checks = {
            'refusal_code_correct': no_bypass.get('refusal_code') == 'REFUSE_NON_BYPASS_VIOLATION',
            'verdict_is_refusal': no_bypass.get('verdict') == 'REFUSAL',
            'witness_valid': _validate_witness(no_bypass)['ok'],
        }

        all_ok = (
            all(permit_checks.values())
            and all(refusal_checks.values())
            and all(replay_checks.values())
            and all(no_bypass_checks.values())
        )
        return {
            'ok': all_ok,
            'permit_algebra': permit_checks,
            'refusal_algebra': refusal_checks,
            'replay_determinism': replay_checks,
            'no_bypass_enforcement': no_bypass_checks,
        }


def _witness_chain_integrity() -> dict[str, Any]:
    """Verify witness certificates across all 6 canonical execution paths."""
    with tempfile.TemporaryDirectory(prefix='wci_') as td:
        bundle = Path(td) / 'bundle'
        compile_bundle(EXAMPLES / 'invoice_profile.json', bundle)
        runner = SealedBoundaryRunner(bundle)
        action = {'action_id': 'wci-test', 'kind': 'emit', 'payload': {}}

        allow_req = load_json(EXAMPLES / 'invoice_request_allow.json')
        deny_req = load_json(EXAMPLES / 'invoice_deny_request.json')

        paths = {
            'verification': verify_bundle(bundle),
            'permit': runner.execute(allow_req, action),
            'refusal': runner.execute(deny_req, action),
            'replay_allow': replay_verdict(bundle, allow_req),
            'replay_deny': replay_verdict(bundle, deny_req),
            'no_bypass': refuse_non_bypass(bundle, allow_req, 'wci-direct'),
        }

        results = {}
        for name, payload in paths.items():
            results[name] = _validate_witness(payload)

        return {
            'ok': all(r['ok'] for r in results.values()),
            'paths': results,
        }


def _corpus_theorem_family_coverage() -> dict[str, Any]:
    """Verify all theorem families have passing evidence in the discharge ledger."""
    ledger_path = ROOT / 'PROOFS' / 'THEOREM_DISCHARGE_LEDGER.json'
    if not ledger_path.exists():
        return {'ok': False, 'error': 'ledger_not_found'}
    ledger = json.loads(ledger_path.read_text(encoding='utf-8'))
    families = ledger.get('families', {})
    strong_count = 0
    partial_count = 0
    failed = []
    for name, entry in families.items():
        status = entry.get('status', '')
        if status == 'EXECUTABLE_WITNESS_STRONG':
            strong_count += 1
        elif status == 'EXECUTABLE_WITNESS_PARTIAL':
            partial_count += 1
        else:
            failed.append({'family': name, 'status': status})
    return {
        'ok': not failed and partial_count == 0,
        'total_families': len(families),
        'strong': strong_count,
        'partial': partial_count,
        'failed': failed,
    }


def run_gate() -> dict[str, Any]:
    # 1. Full mechanized discharge (K1-K14)
    discharge = run_full_family_discharge(ROOT)

    # 2. All existing gate reports
    gates = _verify_all_existing_gates()

    # 3. Refusal/permit algebra
    algebra = _refusal_permit_algebra_test()

    # 4. Witness-certificate chain integrity
    witness = _witness_chain_integrity()

    # 5. Theorem family coverage
    coverage = _corpus_theorem_family_coverage()

    overall_ok = (
        discharge['overall_ok']
        and gates['ok']
        and algebra['ok']
        and witness['ok']
        and coverage['ok']
    )

    report = {
        'overall_ok': overall_ok,
        'gate_name': 'whole_family_theorem_discharge_gate',
        'discharge_grade': 'FULL_FAMILY_MECHANIZED_EXECUTABLE_WITNESS' if overall_ok else 'INCOMPLETE',
        'mechanized_kernel_discharge': discharge,
        'existing_gate_verification': gates,
        'refusal_permit_algebra': algebra,
        'witness_chain_integrity': witness,
        'theorem_family_coverage': coverage,
        'truth_boundary': {
            'status_label': 'full_family_mechanized_executable_witness_discharge',
            'what_is_discharged': [
                'K1-K6: kernel-scoped abstract proof over 4096 finite states',
                'K7: unique ALLOW state (exactly 1 of 4096)',
                'K8: all 12 predicates independently load-bearing',
                'K9: fail-closed monotonicity (weakening any predicate preserves REFUSAL)',
                'K10: verification-admission strict coupling (5 verification predicates)',
                'K11: full canonicalization mechanization over complete corpus',
                'K12: digest binding determinism and collision-resistance',
                'K13: refusal algebra completeness (every REFUSAL has identifiable cause)',
                'K14: cross-implementation equivalence (primary vs independent vs node)',
                'All 12+ existing gates pass with concrete evidence',
                'Refusal/permit algebra verified on real bundle execution',
                'Witness-certificate chain integrity across all 6 execution paths',
                'All theorem families have EXECUTABLE_WITNESS_STRONG evidence',
            ],
            'formal_coverage': {
                'abstract_states': 4096,
                'theorems_mechanized': 14,
                'execution_paths_witnessed': 6,
                'implementation_lines_parity_tested': 3,
                'gate_reports_verified': '12+ required',
            },
            'what_is_not_claimed': [
                'Formal theorem-prover (Lean/Coq/Isabelle) machine-checked proof',
            ],
        },
    }

    text = json.dumps(report, indent=2) + '\n'
    OUT_D.parent.mkdir(parents=True, exist_ok=True)
    OUT_R.parent.mkdir(parents=True, exist_ok=True)
    OUT_D.write_text(text, encoding='utf-8')
    OUT_R.write_text(text, encoding='utf-8')
    return report


if __name__ == '__main__':
    report = run_gate()
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report['overall_ok'] else 1)
