
import { digestData, loadJson, PRIMITIVE_IDENTITY } from './common.mjs';
import { evaluateRequest } from './profile_eval.mjs';
import { makePermit, makeRefusal } from './refusal.mjs';
import { attachWitnessCertificate } from './witness_certificate.mjs';
import { verifyBundleNode } from './verifier.mjs';

export class NodeSecondLineRunner {
  constructor(bundleDir) {
    this.bundleDir = bundleDir;
    this.verification = verifyBundleNode(bundleDir);
    this.bundleManifest = loadJson(`${bundleDir}/MANIFEST.sha256.json`);
    this.bundleDigest = digestData(this.bundleManifest);
    this.profile = loadJson(`${bundleDir}/PROFILE_SOURCE.json`);
  }
  validateRequest(request) {
    if (!request || typeof request !== 'object' || Array.isArray(request)) return 'REFUSE_SCHEMA_INVALID';
    const encoded = Buffer.from(JSON.stringify(request));
    if (encoded.length > 64 * 1024) return 'REFUSE_REQUEST_OVERSIZE';
    if (!request.object || typeof request.object !== 'object' || Array.isArray(request.object)) return 'REFUSE_SCHEMA_INVALID';
    return null;
  }
  execute(request, action) {
    const request_digest = digestData(request);
    if (!this.verification.overall_ok) {
      const out = makeRefusal({ code: this.verification.refusal_code || 'REFUSE_BUNDLE_VERIFICATION_FAILED', layer: 'bundle', bundle_digest: this.verification.bundle_digest, request_digest, verification_result: 'NOT_VERIFIED', refusal_reasons: this.verification.refusal_reasons || ['REFUSE_BUNDLE_VERIFICATION_FAILED'], details: { source: 'node-second-line.execute' } });
      out.overall_ok = false; return attachWitnessCertificate(out);
    }
    const requestProblem = this.validateRequest(request);
    if (requestProblem) {
      const out = makeRefusal({ code: requestProblem, layer: 'runtime', bundle_digest: this.bundleDigest, request_digest, refusal_reasons: [requestProblem], details: { source: 'node-second-line.execute' } });
      out.overall_ok = false; return attachWitnessCertificate(out);
    }
    if (!action || typeof action !== 'object' || Array.isArray(action) || JSON.stringify(Object.keys(action).sort()) !== JSON.stringify(['action_id','kind','payload'])) {
      const out = makeRefusal({ code: 'REFUSE_ACTION_DESCRIPTOR_INVALID', layer: 'action', bundle_digest: this.bundleDigest, request_digest, action_digest: null, refusal_reasons: ['REFUSE_ACTION_DESCRIPTOR_INVALID'], details: { source: 'node-second-line.execute' } });
      out.overall_ok = false; return attachWitnessCertificate(out);
    }
    const result = evaluateRequest(this.profile, request);
    if (result.verdict !== 'ALLOW') {
      const out = makeRefusal({ code: 'REFUSE_VERDICT_NOT_ALLOW', layer: 'action', bundle_digest: this.bundleDigest, request_digest, action_digest: digestData(action), refusal_reasons: ['REFUSE_VERDICT_NOT_ALLOW'], details: { source: 'node-second-line.execute', decisive_rule_ids: result.decisive_rule_ids, matched: result.matched, failed: result.failed, fail_closed: result.fail_closed } });
      out.overall_ok = false; return attachWitnessCertificate(out);
    }
    return attachWitnessCertificate(makePermit({ bundle_digest: this.bundleDigest, request_digest, action, decisive_rule_ids: result.decisive_rule_ids }));
  }
}

export function replayVerdictNode(bundleDir, request) {
  const runner = new NodeSecondLineRunner(bundleDir);
  const request_digest = digestData(request);
  if (!runner.verification.overall_ok) {
    const out = makeRefusal({ code: runner.verification.refusal_code || 'REFUSE_BUNDLE_VERIFICATION_FAILED', layer: 'bundle', bundle_digest: runner.verification.bundle_digest, request_digest, verification_result: 'NOT_VERIFIED', refusal_reasons: runner.verification.refusal_reasons || ['REFUSE_BUNDLE_VERIFICATION_FAILED'], details: { source: 'node-second-line.replay' } });
    out.overall_ok = false; return attachWitnessCertificate(out);
  }
  const requestProblem = runner.validateRequest(request);
  if (requestProblem) {
    const out = makeRefusal({ code: requestProblem, layer: 'runtime', bundle_digest: runner.bundleDigest, request_digest, refusal_reasons: [requestProblem], details: { source: 'node-second-line.replay' } });
    out.overall_ok = false; return attachWitnessCertificate(out);
  }
  const result = evaluateRequest(runner.profile, request);
  if (result.verdict !== 'ALLOW') {
    const out = makeRefusal({ code: 'REFUSE_VERDICT_NOT_ALLOW', layer: 'runtime', bundle_digest: runner.bundleDigest, request_digest, refusal_reasons: ['REFUSE_VERDICT_NOT_ALLOW'], details: { source: 'node-second-line.replay', decisive_rule_ids: result.decisive_rule_ids, matched: result.matched, failed: result.failed, fail_closed: result.fail_closed } });
    out.overall_ok = false; return attachWitnessCertificate(out);
  }
  return attachWitnessCertificate({
    primitive_identity: PRIMITIVE_IDENTITY,
    overall_ok: true,
    bundle_digest: runner.bundleDigest,
    request_digest,
    verdict: 'ALLOW',
    replay_binding: { primitive_identity: PRIMITIVE_IDENTITY, bundle_digest: runner.bundleDigest, request_digest },
    decisive_rule_ids: [...result.decisive_rule_ids],
    matched: [...result.matched],
    failed: [...result.failed],
    fail_closed: result.fail_closed,
  });
}
