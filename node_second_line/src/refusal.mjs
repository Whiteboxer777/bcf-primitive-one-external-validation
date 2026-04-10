
import { PRIMITIVE_IDENTITY, digestData } from './common.mjs';

export const CODE_TO_CLASS = {
  REFUSE_PRIMITIVE_IDENTITY_INVALID: 'primitive_identity',
  REFUSE_CANONICALIZATION_FAILED: 'canonicalization',
  REFUSE_REQUIRED_FILES_MISSING: 'verification',
  REFUSE_UNDECLARED_FILE: 'verification',
  REFUSE_CONTRACT_MISMATCH: 'verification',
  REFUSE_MANIFEST_MISMATCH: 'verification',
  REFUSE_COMPILER_PRODUCT_MISMATCH: 'verification',
  REFUSE_CERTIFICATE_INVALID: 'verification',
  REFUSE_GOVERNANCE_INVALID: 'verification',
  REFUSE_VERDICT_SCHEMA_INVALID: 'verification',
  REFUSE_VERIFICATION_SCHEMA_INVALID: 'verification',
  REFUSE_REFUSAL_SCHEMA_INVALID: 'verification',
  REFUSE_PERMIT_SCHEMA_INVALID: 'verification',
  REFUSE_CLAIM_TCB_INVALID: 'verification',
  REFUSE_CLAIM_MATRIX_INVALID: 'verification',
  REFUSE_WITNESS_REPLAY_FAILED: 'verification',
  REFUSE_BUNDLE_VERIFICATION_FAILED: 'verification',
  REFUSE_SCHEMA_INVALID: 'request_shape',
  REFUSE_REQUEST_OVERSIZE: 'request_bounds',
  REFUSE_ACTION_DESCRIPTOR_INVALID: 'action_binding',
  REFUSE_VERDICT_NOT_ALLOW: 'contract_satisfaction',
  REFUSE_NON_BYPASS_VIOLATION: 'non_bypass',
  REFUSE_EQUIVALENCE_PARITY_FAILED: 'equivalence',
};

export function makeRefusal({ code, layer, bundle_digest, request_digest = null, action_digest = null, attempted_entrypoint = null, verification_result = null, refusal_reasons = null, details = null, permit_binding = null }) {
  if (!(code in CODE_TO_CLASS)) throw new Error(`unknown refusal code: ${code}`);
  const refusal = {
    primitive_identity: PRIMITIVE_IDENTITY,
    bundle_digest,
    request_digest,
    action_digest,
    permit: false,
    verdict: 'REFUSAL',
    refusal_code: code,
    refusal_class: CODE_TO_CLASS[code],
    layer,
    permit_binding,
    replay_binding: {
      primitive_identity: PRIMITIVE_IDENTITY,
      bundle_digest,
      request_digest,
    },
  };
  if (attempted_entrypoint !== null) refusal.attempted_entrypoint = attempted_entrypoint;
  if (verification_result !== null) refusal.verification_result = verification_result;
  if (refusal_reasons !== null) refusal.refusal_reasons = [...refusal_reasons];
  if (details) refusal.details = details;
  return refusal;
}

export function makePermit({ bundle_digest, request_digest, action, decisive_rule_ids }) {
  const action_digest = digestData(action);
  return {
    primitive_identity: PRIMITIVE_IDENTITY,
    bundle_digest,
    request_digest,
    action_digest,
    permit: true,
    verdict: 'ALLOW',
    permit_type: 'ACTION_DESCRIPTOR_RELEASE',
    released_action: action,
    action_authority: {
      kind: 'release_bound_action_descriptor',
      action_id: action.action_id,
      action_kind: action.kind,
    },
    permit_binding: {
      primitive_identity: PRIMITIVE_IDENTITY,
      bundle_digest,
      request_digest,
      action_digest,
    },
    replay_binding: {
      primitive_identity: PRIMITIVE_IDENTITY,
      bundle_digest,
      request_digest,
    },
    decisive_rule_ids: [...decisive_rule_ids],
  };
}
