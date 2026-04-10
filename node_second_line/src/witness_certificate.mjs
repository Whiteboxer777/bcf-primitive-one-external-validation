
import { PRIMITIVE_IDENTITY, digestData } from './common.mjs';

export const CERTIFICATE_VERSION = 'WITNESS_CERT_V2';
export const CERTIFICATE_SCOPE = 'kernel_evidence_carrying_v2';

function stripWitnessCertificate(payload) {
  const { witness_certificate, ...rest } = payload;
  return rest;
}

function bindingPayload(source) {
  if (source.permit_binding && typeof source.permit_binding === 'object') return source.permit_binding;
  if (source.replay_binding && typeof source.replay_binding === 'object') return source.replay_binding;
  if ('bundle_digest' in source) return { primitive_identity: PRIMITIVE_IDENTITY, bundle_digest: source.bundle_digest ?? null, request_digest: source.request_digest ?? null, action_digest: source.action_digest ?? null };
  return null;
}

function finalizeClaims(claims) {
  const out = { ...claims };
  out.claim_set_digest = digestData(out);
  return out;
}

function buildWitnessCertificate({ certificate_type, source_verdict, source_kind, payload, witness_claims }) {
  const source = stripWitnessCertificate(payload);
  const binding = bindingPayload(source);
  const body = {
    primitive_identity: PRIMITIVE_IDENTITY,
    certificate_version: CERTIFICATE_VERSION,
    certificate_scope: CERTIFICATE_SCOPE,
    certificate_type,
    source_verdict,
    source_kind,
    bundle_digest: source.bundle_digest ?? null,
    request_digest: source.request_digest ?? null,
    action_digest: source.action_digest ?? null,
    source_digest: digestData(source),
    binding_digest: binding ? digestData(binding) : null,
    witness_claims: finalizeClaims(witness_claims),
  };
  body.certificate_digest = digestData(body);
  return body;
}

export function attachWitnessCertificate(payload) {
  const source = stripWitnessCertificate(payload);
  let cert;
  if (source.verification_result === 'VERIFIED') {
    const checks = source.checks && typeof source.checks === 'object' ? source.checks : {};
    const details = source.details && typeof source.details === 'object' ? source.details : {};
    cert = buildWitnessCertificate({
      certificate_type: 'verification_witness',
      source_verdict: 'VERIFIED',
      source_kind: 'verification_result',
      payload: source,
      witness_claims: {
        witness_kind: 'verification',
        witness_scope: 'bundle_verification',
        binding_kind: 'bundle_only',
        verification_result: 'VERIFIED',
        checks_digest: digestData(checks),
        details_digest: digestData(details),
        check_truth_count: Object.values(checks).filter(v => v === true).length,
      },
    });
  } else if (source.verdict === 'ALLOW' && source.action_authority && typeof source.action_authority === 'object') {
    const decisive = Array.isArray(source.decisive_rule_ids) ? [...source.decisive_rule_ids] : [];
    cert = buildWitnessCertificate({
      certificate_type: 'permit_witness',
      source_verdict: 'ALLOW',
      source_kind: 'permit',
      payload: source,
      witness_claims: {
        witness_kind: 'permit',
        witness_scope: 'action_release',
        binding_kind: 'action_release',
        action_authority_kind: source.action_authority.kind ?? null,
        decisive_rule_ids: decisive,
        decisive_rule_ids_digest: digestData(decisive),
        permit_binding_digest: digestData(source.permit_binding ?? source.replay_binding ?? {}),
      },
    });
  } else if (source.verdict === 'ALLOW') {
    const decisive = Array.isArray(source.decisive_rule_ids) ? [...source.decisive_rule_ids] : [];
    cert = buildWitnessCertificate({
      certificate_type: 'permit_witness',
      source_verdict: 'ALLOW',
      source_kind: 'replay_allow',
      payload: source,
      witness_claims: {
        witness_kind: 'permit',
        witness_scope: 'replay_allow',
        binding_kind: 'replay',
        action_authority_kind: null,
        decisive_rule_ids: decisive,
        decisive_rule_ids_digest: digestData(decisive),
        permit_binding_digest: digestData(source.replay_binding ?? {}),
      },
    });
  } else {
    let source_kind = 'refusal';
    let witness_scope = 'action_refusal';
    let binding_kind = 'action_release';
    if (source.attempted_entrypoint !== undefined) {
      source_kind = 'non_bypass_refusal';
      witness_scope = 'non_bypass_refusal';
      binding_kind = 'non_bypass';
    } else if (source.layer === 'bundle' || source.verification_result === 'NOT_VERIFIED') {
      source_kind = 'refusal';
      witness_scope = 'bundle_refusal';
      binding_kind = 'bundle_failure';
    } else if (source.layer === 'runtime') {
      source_kind = 'replay_refusal';
      witness_scope = 'replay_refusal';
      binding_kind = 'replay';
    }
    const reasons = Array.isArray(source.refusal_reasons) ? [...source.refusal_reasons] : [];
    cert = buildWitnessCertificate({
      certificate_type: 'refusal_witness',
      source_verdict: 'REFUSAL',
      source_kind,
      payload: source,
      witness_claims: {
        witness_kind: 'refusal',
        witness_scope,
        binding_kind,
        refusal_code: source.refusal_code,
        refusal_class: source.refusal_class,
        refusal_reasons_digest: digestData(reasons),
        details_digest: digestData(source.details ?? {}),
      },
    });
  }
  return { ...source, witness_certificate: cert };
}
