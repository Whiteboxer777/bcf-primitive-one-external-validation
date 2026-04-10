from __future__ import annotations
from dataclasses import dataclass
from typing import Final
from .common import digest_data

CONTRACT_VERSION: Final[str] = 'BCF_PRIMITIVE_ONE_CONTRACT_V1'
MANIFEST_NAME: Final[str] = 'MANIFEST.sha256.json'
VERDICT_SCHEMA_NAME: Final[str] = 'VERDICT.schema.json'
VERIFICATION_SCHEMA_NAME: Final[str] = 'VERIFICATION_RESULT.schema.json'
REFUSAL_SCHEMA_NAME: Final[str] = 'REFUSAL.schema.json'
PERMIT_SCHEMA_NAME: Final[str] = 'PERMIT.schema.json'
COMPILED_BACKEND_SCHEMA_NAME: Final[str] = 'COMPILED_BACKEND.schema.json'
WITNESS_CERTIFICATE_SCHEMA_NAME: Final[str] = 'WITNESS_CERTIFICATE.schema.json'
FROZEN_LAW_SHEET: Final[str] = 'SPEC/PRIMITIVE_LAW.md'
THEOREM_SHEET: Final[str] = 'SPEC/THEOREM_SET.md'
CLAIM_MATRIX_NAME: Final[str] = 'CLAIM_TEST_MATRIX.json'
TCB_REPORT_NAME: Final[str] = 'TCB_REPORT.json'
CLAIM_NAME: Final[str] = 'CLAIM.json'

MANIFEST_SCOPED_FILES: Final[tuple[str, ...]] = (
    'PROFILE_SOURCE.json', 'NORMAL_FORM.json', 'ADMISSION_NORMAL_FORM.json', 'COMPILED_BACKEND.json', 'MINIMIZED_FORM.json', 'SAT_REPORT.json',
    'RELATION_REPORT.json', 'WITNESS_SET.json', 'DECISIVE_CORE_SAMPLE.json',
    'NORMALIZATION_CERT.json', 'MINIMIZATION_CERT.json', 'SAT_CERT.json', 'RELATION_CERT.json',
    'CONFORMANCE_CERT.json', 'DECISIVE_CORE_CERT.json', 'TRUST_ROOTS.json', 'AUTHORITY_POLICY.json',
    'REVOCATION_LIST.json', 'BUILD_INFO.json', 'BUNDLE_CONTRACT.json', CLAIM_NAME, TCB_REPORT_NAME,
    VERDICT_SCHEMA_NAME, VERIFICATION_SCHEMA_NAME, REFUSAL_SCHEMA_NAME, PERMIT_SCHEMA_NAME, 'ADMISSION_NORMAL_FORM.schema.json', COMPILED_BACKEND_SCHEMA_NAME, WITNESS_CERTIFICATE_SCHEMA_NAME,
    'VERIFICATION_WITNESS_CERT.json', 'PERMIT_WITNESS_CERT.json', 'REFUSAL_WITNESS_CERT.json',
    'REPLAY_ALLOW_WITNESS_CERT.json', 'REPLAY_REFUSAL_WITNESS_CERT.json', 'NO_BYPASS_WITNESS_CERT.json',
    CLAIM_MATRIX_NAME,
)
GOVERNANCE_FILES: Final[tuple[str, ...]] = ('PROMOTION_CERT.json', 'PROMOTION_SIGNATURES.json', 'SUPERSESSION_CHAIN.json')
REQUIRED_FILES: Final[tuple[str, ...]] = MANIFEST_SCOPED_FILES + (MANIFEST_NAME,) + GOVERNANCE_FILES
ALLOWED_TOP_LEVEL_FILES: Final[tuple[str, ...]] = REQUIRED_FILES + ('SEALED_RUNNER_AUDIT.jsonl',)
RUNTIME_REQUEST_LIMITS: Final[dict[str, int]] = {'max_request_bytes': 64 * 1024, 'max_decision_log_entries': 10_000}

VERDICT_SCHEMA: Final[dict[str, object]] = {
    '$schema': 'https://json-schema.org/draft/2020-12/schema',
    'title': 'BCF Primitive One Verdict',
    'type': 'object',
    'required': ['bundle_digest', 'request_digest', 'verdict', 'decisive_rule_ids', 'matched', 'failed', 'fail_closed'],
    'properties': {
        'bundle_digest': {'type': 'string'},
        'request_digest': {'type': 'string'},
        'verdict': {'enum': ['ALLOW', 'DENY']},
        'decisive_rule_ids': {'type': 'array', 'items': {'type': 'string'}},
        'matched': {'type': 'array', 'items': {'type': 'string'}},
        'failed': {'type': 'array', 'items': {'type': 'string'}},
        'fail_closed': {'type': 'boolean'},
    },
    'additionalProperties': False,
}

@dataclass(frozen=True)
class BundleContract:
    version: str
    manifest_name: str
    manifest_scoped_files: tuple[str, ...]
    governance_files: tuple[str, ...]
    required_files: tuple[str, ...]
    allowed_top_level_files: tuple[str, ...]
    runtime_request_limits: dict[str, int]
    verdict_schema_name: str
    verification_schema_name: str
    refusal_schema_name: str
    permit_schema_name: str
    compiled_backend_schema_name: str
    witness_certificate_schema_name: str
    frozen_law_sheet: str
    theorem_sheet: str
    claim_name: str
    tcb_report_name: str
    claim_matrix_name: str

    def to_dict(self) -> dict[str, object]:
        data = {
            'contract_version': self.version,
            'manifest_name': self.manifest_name,
            'manifest_scoped_files': list(self.manifest_scoped_files),
            'governance_files': list(self.governance_files),
            'required_files': list(self.required_files),
            'allowed_top_level_files': list(self.allowed_top_level_files),
            'runtime_request_limits': dict(self.runtime_request_limits),
            'verdict_schema_name': self.verdict_schema_name,
            'verification_schema_name': self.verification_schema_name,
            'refusal_schema_name': self.refusal_schema_name,
            'permit_schema_name': self.permit_schema_name,
            'compiled_backend_schema_name': self.compiled_backend_schema_name,
            'witness_certificate_schema_name': self.witness_certificate_schema_name,
            'frozen_law_sheet': self.frozen_law_sheet,
            'theorem_sheet': self.theorem_sheet,
            'claim_name': self.claim_name,
            'tcb_report_name': self.tcb_report_name,
            'claim_matrix_name': self.claim_matrix_name,
            'semantics': {
                'decision_function': 'ALLOW_OR_DENY_ONLY',
                'failure_law': 'ERROR_EQ_DENY_OR_REFUSAL',
                'closed_world': True,
                'bundle_success_law': 'compile_success_implies_verifier_complete_bundle',
                'official_route': 'source_profile -> canonical_bundle -> verify -> sealed_runner -> permit_or_refusal',
                'parallel_families': 'forbidden_in_primitive_release_root',
                'top_level_extras': 'forbidden_except_audit_log',
                'official_runner': 'sealed-runner-only',
                'runtime_direct_entrypoints': 'not_officially_exposed',
                'verifier_independence': 'standalone_verifier_release_is_normative_external_verifier',
                'schema_harness': 'verification_permit_refusal_compiled_backend_schema_validation_required',
                'compiled_backend': 'indexed_dnf_clause_backend_required_for_current_compiled_execution_line',
                'witness_certificate': 'verification_permit_refusal_witness_certificate_required_for_current_evidence_carrying_line',
                'equivalence_target': 'runtime_surface_vs_verifier_surface_parity_required',
            },
        }
        data['contract_digest'] = digest_data(data)
        return data

bundle_contract = BundleContract(
    version=CONTRACT_VERSION,
    manifest_name=MANIFEST_NAME,
    manifest_scoped_files=MANIFEST_SCOPED_FILES,
    governance_files=GOVERNANCE_FILES,
    required_files=REQUIRED_FILES,
    allowed_top_level_files=ALLOWED_TOP_LEVEL_FILES,
    runtime_request_limits=RUNTIME_REQUEST_LIMITS,
    verdict_schema_name=VERDICT_SCHEMA_NAME,
    verification_schema_name=VERIFICATION_SCHEMA_NAME,
    refusal_schema_name=REFUSAL_SCHEMA_NAME,
    permit_schema_name=PERMIT_SCHEMA_NAME,
    compiled_backend_schema_name=COMPILED_BACKEND_SCHEMA_NAME,
    witness_certificate_schema_name=WITNESS_CERTIFICATE_SCHEMA_NAME,
    frozen_law_sheet=FROZEN_LAW_SHEET,
    theorem_sheet=THEOREM_SHEET,
    claim_name=CLAIM_NAME,
    tcb_report_name=TCB_REPORT_NAME,
    claim_matrix_name=CLAIM_MATRIX_NAME,
)
