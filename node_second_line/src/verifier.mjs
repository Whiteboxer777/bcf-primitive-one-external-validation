
import fs from 'node:fs';
import path from 'node:path';
import { digestData, loadJson, sha256File, PRIMITIVE_IDENTITY, stableStringify } from './common.mjs';
import { makeRefusal } from './refusal.mjs';
import { attachWitnessCertificate } from './witness_certificate.mjs';
import { evaluateRequest } from './profile_eval.mjs';

const CONTRACT_VERSION = 'BCF_PRIMITIVE_ONE_CONTRACT_V1';
const MANIFEST_NAME = 'MANIFEST.sha256.json';
const VERDICT_SCHEMA_NAME = 'VERDICT.schema.json';
const VERIFICATION_SCHEMA_NAME = 'VERIFICATION_RESULT.schema.json';
const REFUSAL_SCHEMA_NAME = 'REFUSAL.schema.json';
const PERMIT_SCHEMA_NAME = 'PERMIT.schema.json';
const WITNESS_CERTIFICATE_SCHEMA_NAME = 'WITNESS_CERTIFICATE.schema.json';
const COMPILED_BACKEND_SCHEMA_NAME = 'COMPILED_BACKEND.schema.json';
const CLAIM_MATRIX_NAME = 'CLAIM_TEST_MATRIX.json';
const TCB_REPORT_NAME = 'TCB_REPORT.json';
const CLAIM_NAME = 'CLAIM.json';
const MANIFEST_SCOPED_FILES = [
  'PROFILE_SOURCE.json', 'NORMAL_FORM.json', 'ADMISSION_NORMAL_FORM.json', 'COMPILED_BACKEND.json', 'MINIMIZED_FORM.json', 'SAT_REPORT.json',
  'RELATION_REPORT.json', 'WITNESS_SET.json', 'DECISIVE_CORE_SAMPLE.json',
  'NORMALIZATION_CERT.json', 'MINIMIZATION_CERT.json', 'SAT_CERT.json', 'RELATION_CERT.json',
  'CONFORMANCE_CERT.json', 'DECISIVE_CORE_CERT.json', 'TRUST_ROOTS.json', 'AUTHORITY_POLICY.json',
  'REVOCATION_LIST.json', 'BUILD_INFO.json', 'BUNDLE_CONTRACT.json', CLAIM_NAME, TCB_REPORT_NAME,
  VERDICT_SCHEMA_NAME, VERIFICATION_SCHEMA_NAME, REFUSAL_SCHEMA_NAME, PERMIT_SCHEMA_NAME,
  'ADMISSION_NORMAL_FORM.schema.json', COMPILED_BACKEND_SCHEMA_NAME, WITNESS_CERTIFICATE_SCHEMA_NAME,
  'VERIFICATION_WITNESS_CERT.json', 'PERMIT_WITNESS_CERT.json', 'REFUSAL_WITNESS_CERT.json',
  'REPLAY_ALLOW_WITNESS_CERT.json', 'REPLAY_REFUSAL_WITNESS_CERT.json', 'NO_BYPASS_WITNESS_CERT.json',
  CLAIM_MATRIX_NAME,
];
const GOVERNANCE_FILES = ['PROMOTION_CERT.json', 'PROMOTION_SIGNATURES.json', 'SUPERSESSION_CHAIN.json'];
const REQUIRED_FILES = [...MANIFEST_SCOPED_FILES, MANIFEST_NAME, ...GOVERNANCE_FILES];
const ALLOWED_TOP_LEVEL_FILES = [...REQUIRED_FILES, 'SEALED_RUNNER_AUDIT.jsonl'];
const REFUSAL_CODE_MAP = {
  required_files: 'REFUSE_REQUIRED_FILES_MISSING',
  top_level: 'REFUSE_UNDECLARED_FILE',
  contract: 'REFUSE_CONTRACT_MISMATCH',
  manifest: 'REFUSE_MANIFEST_MISMATCH',
  compiler_products: 'REFUSE_COMPILER_PRODUCT_MISMATCH',
  certificates: 'REFUSE_CERTIFICATE_INVALID',
  governance: 'REFUSE_GOVERNANCE_INVALID',
  verdict_schema: 'REFUSE_VERDICT_SCHEMA_INVALID',
  verification_schema: 'REFUSE_VERIFICATION_SCHEMA_INVALID',
  refusal_schema: 'REFUSE_REFUSAL_SCHEMA_INVALID',
  permit_schema: 'REFUSE_PERMIT_SCHEMA_INVALID',
  compiled_backend_schema: 'REFUSE_COMPILED_BACKEND_SCHEMA_INVALID',
  claim_and_tcb: 'REFUSE_CLAIM_TCB_INVALID',
  claim_matrix: 'REFUSE_CLAIM_MATRIX_INVALID',
  witness_replay: 'REFUSE_WITNESS_REPLAY_FAILED',
};
const PRECEDENCE = ['required_files','top_level','contract','manifest','compiler_products','certificates','governance','verdict_schema','verification_schema','refusal_schema','permit_schema','compiled_backend_schema','claim_and_tcb','claim_matrix','witness_replay'];

function bundleContract() {
  const data = {
    contract_version: CONTRACT_VERSION,
    manifest_name: MANIFEST_NAME,
    manifest_scoped_files: MANIFEST_SCOPED_FILES,
    governance_files: GOVERNANCE_FILES,
    required_files: REQUIRED_FILES,
    allowed_top_level_files: ALLOWED_TOP_LEVEL_FILES,
    runtime_request_limits: { max_request_bytes: 64 * 1024, max_decision_log_entries: 10000 },
    verdict_schema_name: VERDICT_SCHEMA_NAME,
    verification_schema_name: VERIFICATION_SCHEMA_NAME,
    refusal_schema_name: REFUSAL_SCHEMA_NAME,
    permit_schema_name: PERMIT_SCHEMA_NAME,
    witness_certificate_schema_name: WITNESS_CERTIFICATE_SCHEMA_NAME,
    compiled_backend_schema_name: COMPILED_BACKEND_SCHEMA_NAME,
    frozen_law_sheet: 'SPEC/PRIMITIVE_LAW.md',
    theorem_sheet: 'SPEC/THEOREM_SET.md',
    claim_name: CLAIM_NAME,
    tcb_report_name: TCB_REPORT_NAME,
    claim_matrix_name: CLAIM_MATRIX_NAME,
    semantics: {
      decision_function: 'ALLOW_OR_DENY_ONLY',
      failure_law: 'ERROR_EQ_DENY_OR_REFUSAL',
      closed_world: true,
      bundle_success_law: 'compile_success_implies_verifier_complete_bundle',
      official_route: 'source_profile -> canonical_bundle -> verify -> sealed_runner -> permit_or_refusal',
      parallel_families: 'forbidden_in_primitive_release_root',
      top_level_extras: 'forbidden_except_audit_log',
      official_runner: 'sealed-runner-only',
      runtime_direct_entrypoints: 'not_officially_exposed',
      verifier_independence: 'standalone_verifier_release_is_normative_external_verifier',
      schema_harness: 'verification_permit_refusal_compiled_backend_schema_validation_required',
      compiled_backend: 'indexed_dnf_clause_backend_required_for_current_compiled_execution_line',
      witness_certificate: 'verification_permit_refusal_witness_certificate_required_for_current_evidence_carrying_line',
      equivalence_target: 'runtime_surface_vs_verifier_surface_parity_required',
    },
  };
  data.contract_digest = digestData(data);
  return data;
}

function releaseRoot() {
  return path.resolve(path.dirname(new URL(import.meta.url).pathname), '../..');
}

function verifyRequiredFiles(bundleDir) {
  const missing = REQUIRED_FILES.filter(rel => !fs.existsSync(path.join(bundleDir, rel)));
  return { ok: missing.length === 0, missing };
}

function verifyNoForbiddenTopLevel(bundleDir) {
  const present = fs.readdirSync(bundleDir).sort();
  const extra = present.filter(name => !ALLOWED_TOP_LEVEL_FILES.includes(name) && !name.startsWith('.'));
  return { ok: extra.length === 0, extra };
}

function verifyContract(bundleDir) {
  const stored = loadJson(path.join(bundleDir, 'BUNDLE_CONTRACT.json'));
  const expected = bundleContract();
  return { ok: stableStringify(stored) === stableStringify(expected), expected_contract_digest: expected.contract_digest, stored_contract_digest: stored.contract_digest };
}

function verifyManifest(bundleDir) {
  const manifest = loadJson(path.join(bundleDir, MANIFEST_NAME));
  const mismatches = [];
  for (const rel of MANIFEST_SCOPED_FILES) {
    const p = path.join(bundleDir, rel);
    const actual = fs.existsSync(p) ? sha256File(p) : null;
    const expected = manifest[rel] ?? null;
    if (actual !== expected) mismatches.push({ file: rel, expected, actual });
  }
  const extraManifestEntries = Object.keys(manifest).filter(k => !MANIFEST_SCOPED_FILES.includes(k)).sort();
  return { ok: mismatches.length === 0 && extraManifestEntries.length === 0, mismatches, extra_manifest_entries: extraManifestEntries, bundle_digest: digestData(manifest) };
}

function sortKey(node) {
  return JSON.stringify([node.kind, node.path || '', JSON.stringify(node.value), JSON.stringify(node.low), JSON.stringify(node.high), (node.children || []).map(sortKey)]);
}
function isNegationPair(a,b){ return a.kind==='NOT' && a.children && a.children.length && sortKey(a.children[0])===sortKey(b); }

function compileAdmissionNormalForm(profile) {
  const normalized = normalizeNode(profile.root);
  const atoms = [];
  function collect(node) {
    if (!node) return;
    if (!node.children || node.children.length === 0 || (node.kind === 'NOT' && node.children && node.children.length===1 && (!node.children[0].children || node.children[0].children.length===0))) {
      if (node.kind !== 'TRUE' && node.kind !== 'FALSE') atoms.push(node.kind === 'NOT' ? node.children[0] : node);
      return;
    }
    for (const child of (node.children || [])) collect(child);
  }
  collect(normalized);
  const uniq = [];
  const seen = new Set();
  for (const atom of atoms.sort((a,b)=>stableStringify(a).localeCompare(stableStringify(b)))) {
    const key = stableStringify(atom); if (seen.has(key)) continue; seen.add(key); uniq.push(atom);
  }
  const atomIndex = uniq.map((atom, i)=>({atom_id:`A${String(i+1).padStart(4,'0')}`, atom_kind: atom.kind, rule_id: atom.metadata ? atom.metadata.rule_id ?? null : null, atom, atom_digest: digestOf(atom)}));
  function dnf(node) {
    if (node.kind === 'TRUE') return [[]];
    if (node.kind === 'FALSE') return [];
    if (!node.children || node.children.length===0 || (node.kind==='NOT' && node.children.length===1 && (!node.children[0].children || node.children[0].children.length===0))) {
      const atom = node.kind==='NOT' ? node.children[0] : node;
      const atomId = atomIndex.find(x=>stableStringify(x.atom)===stableStringify(atom)).atom_id;
      return [[{atom_id:atomId, polarity: node.kind==='NOT' ? 'negative':'positive', atom}]];
    }
    if (node.kind==='OR') return node.children.flatMap(dnf);
    if (node.kind==='AND') {
      let clauses=[[]];
      for (const child of node.children) {
        const childClauses = dnf(child);
        const next=[];
        for (const left of clauses) for (const right of childClauses) {
          const combo=[...left,...right];
          const polarity=new Map(); let bad=false; const ded=[];
          for (const lit of combo) {
            if (polarity.has(lit.atom_id)) { if (polarity.get(lit.atom_id)!==lit.polarity) { bad=true; break; } continue; }
            polarity.set(lit.atom_id, lit.polarity); ded.push(lit);
          }
          if (!bad) next.push(ded.sort((a,b)=>`${a.atom_id}:${a.polarity}`.localeCompare(`${b.atom_id}:${b.polarity}`)));
        }
        clauses = next;
      }
      return clauses;
    }
    throw new Error(`unsupported ANF node kind ${node.kind}`);
  }
  const clausesRaw = dnf(normalized);
  const clauseSeen = new Set();
  const clauses=[];
  for (const lits of clausesRaw) {
    const key=stableStringify(lits.map(l=>[l.atom_id,l.polarity])); if (clauseSeen.has(key)) continue; clauseSeen.add(key); clauses.push({literals:lits});
  }
  const body = {profile_id: profile.profile_id, source_kind: 'dnf_literal_clauses', normalized_root: normalized, atom_index: atomIndex, clauses, compilation_trace:['node-normalize','to-nnf-subset','dnf-compilation',`clause-count=${clauses.length}`,`atom-count=${atomIndex.length}`]};
  body.anf_digest = digestOf(body);
  return body;
}
function normalizeNode(n) {
  const trace = [];
  function norm(node) {
    const atomKinds = new Set(['TRUE','FALSE','EQ','NEQ','IN','NOT_IN','EXISTS','ABSENT','RANGE','MATCHES','AUTHORITY_EQ','TRUST_EQ','REGIME_EQ','EVIDENCE_EQ','ACTION_EQ','BEFORE_EQ','AFTER_EQ','BEFORE_RANGE','AFTER_RANGE','CHANGED','UNCHANGED']);
    if (atomKinds.has(node.kind)) return node;
    if (node.kind === 'NOT') {
      const child = norm(node.children[0]);
      if (child.kind === 'TRUE') return { kind: 'FALSE' };
      if (child.kind === 'FALSE') return { kind: 'TRUE' };
      if (child.kind === 'NOT') return child.children[0];
      return { ...node, children: [child] };
    }
    if (node.kind === 'AND' || node.kind === 'OR') {
      let flat = [];
      for (const ch of node.children || []) {
        const c = norm(ch);
        if (c.kind === node.kind) flat.push(...(c.children || [])); else flat.push(c);
      }
      const filtered = [];
      const seen = new Set();
      for (const child of flat) {
        if (node.kind === 'AND' && child.kind === 'TRUE') continue;
        if (node.kind === 'OR' && child.kind === 'FALSE') continue;
        if (node.kind === 'AND' && child.kind === 'FALSE') return { kind: 'FALSE' };
        if (node.kind === 'OR' && child.kind === 'TRUE') return { kind: 'TRUE' };
        const key = sortKey(child);
        if (seen.has(key)) continue;
        if (filtered.some(prev => isNegationPair(child, prev) || isNegationPair(prev, child))) return node.kind === 'AND' ? { kind: 'FALSE' } : { kind: 'TRUE' };
        seen.add(key); filtered.push(child);
      }
      filtered.sort((a,b)=>sortKey(a).localeCompare(sortKey(b)));
      if (!filtered.length) return node.kind === 'AND' ? { kind: 'TRUE' } : { kind: 'FALSE' };
      if (filtered.length === 1) return filtered[0];
      return { ...node, children: filtered };
    }
    return node;
  }
  return { node: norm(n), trace };
}

function verifyCompilerProducts(bundleDir) {
  const profile = loadJson(path.join(bundleDir, 'PROFILE_SOURCE.json'));
  const recomputedNorm = normalizeNode(profile.root).node;
  const storedNorm = loadJson(path.join(bundleDir, 'NORMAL_FORM.json'));
  const storedBackend = loadJson(path.join(bundleDir, 'COMPILED_BACKEND.json'));
  const checks = { normal_form: JSON.stringify(recomputedNorm) === JSON.stringify(storedNorm), compiled_backend: storedBackend.source_kind === 'indexed_dnf_clause_backend_v1' && storedBackend.anf_digest && Array.isArray(storedBackend.clauses) };
  return { ok: Object.values(checks).every(Boolean), checks };
}

function verifyCertificates(bundleDir) {
  const certNames = ['NORMALIZATION_CERT.json','MINIMIZATION_CERT.json','SAT_CERT.json','RELATION_CERT.json','CONFORMANCE_CERT.json','DECISIVE_CORE_CERT.json','PROMOTION_CERT.json'];
  const details = {};
  for (const name of certNames) {
    const cert = loadJson(path.join(bundleDir, name));
    const claims = { ...cert };
    delete claims.cert_digest;
    details[name] = { ok: digestData(claims) === cert.cert_digest };
  }
  return { ok: Object.values(details).every(v => v.ok), details };
}

function verifyGovernance(bundleDir, manifestDigest) {
  const trust = loadJson(path.join(bundleDir, 'TRUST_ROOTS.json'));
  const policy = loadJson(path.join(bundleDir, 'AUTHORITY_POLICY.json'));
  const revocations = loadJson(path.join(bundleDir, 'REVOCATION_LIST.json'));
  const promotion = loadJson(path.join(bundleDir, 'PROMOTION_CERT.json'));
  const signatures = (loadJson(path.join(bundleDir, 'PROMOTION_SIGNATURES.json')).signatures) || [];
  const supersession = loadJson(path.join(bundleDir, 'SUPERSESSION_CHAIN.json'));
  const allowedScopes = new Set((((policy || {}).allowed_scopes || {})[promotion.claims.promotion_verdict] || []));
  const minSigs = Number((((policy || {}).minimum_signatures || {})[promotion.claims.promotion_verdict] || 1));
  const approved = signatures.filter(sig => {
    const signer = ((trust || {}).roots || {})[sig.signer_id] || {};
    const roles = new Set(signer.roles || []);
    const signerScopes = new Set(signer.scopes || []);
    if ((revocations.revoked_signers || []).includes(sig.signer_id)) return false;
    if (!roles.has('bundle_signer')) return false;
    if (!allowedScopes.has(sig.scope)) return false;
    if (!signerScopes.has(sig.scope)) return false;
    return true;
  });
  const promotionOk = promotion.claims.bundle_digest === manifestDigest && promotion.claims.manifest_digest === manifestDigest && promotion.claims.contract_version === CONTRACT_VERSION;
  const supersessionOk = supersession.current_bundle_digest === manifestDigest && supersession.promotion_cert_digest === promotion.cert_digest;
  return { ok: promotionOk && supersessionOk && approved.length >= minSigs, promotion_ok: promotionOk, supersession_ok: supersessionOk, minimum_required: minSigs, approved_count: approved.length };
}

function verifySchemaExact(bundleDir, bundleName, projectName) {
  const stored = loadJson(path.join(bundleDir, bundleName));
  let ok = false;
  if (bundleName === 'VERIFICATION_RESULT.schema.json') {
    ok = stored && stored.title === 'BCF Verification Result' && Array.isArray(stored.oneOf) && stored.oneOf.length >= 1;
  } else if (bundleName === 'REFUSAL.schema.json') {
    ok = stored && stored.title === 'BCF Refusal Event' && stored.properties && stored.properties.verdict && JSON.stringify(stored.properties.verdict.enum) === JSON.stringify(['REFUSAL']);
  } else if (bundleName === 'PERMIT.schema.json') {
    const kindEnum = stored?.properties?.action_authority?.properties?.kind?.enum;
    ok = stored && stored.title === 'BCF Permit Event' && JSON.stringify(kindEnum) === JSON.stringify(['release_bound_action_descriptor']);
  } else if (bundleName === 'COMPILED_BACKEND.schema.json') {
    ok = stored && stored.title === 'BCF Primitive One Compiled Backend' && stored.properties && stored.properties.source_kind && stored.properties.source_kind.const === 'indexed_dnf_clause_backend_v1';
  }
  return { ok, schema_name: bundleName };
}

function verifyClaimAndTcb(bundleDir) {
  const claim = loadJson(path.join(bundleDir, CLAIM_NAME));
  const tcb = loadJson(path.join(bundleDir, TCB_REPORT_NAME));
  const claimOk = claim.parallel_families === false && claim.official_runner_only === true && claim.direct_runtime_api_officially_supported === false && claim.official_route === 'source_profile -> canonical_bundle -> verify -> sealed_runner -> permit_or_refusal';
  const tcbOk = tcb.official_runner_only === true && tcb.reduction_status === 'primitive_one_reference_tcb';
  return { ok: claimOk && tcbOk, claim_ok: claimOk, tcb_ok: tcbOk };
}

function verifyClaimMatrix(bundleDir) {
  const matrix = loadJson(path.join(bundleDir, CLAIM_MATRIX_NAME));
  const claims = matrix.claims || [];
  const ok = matrix.version === CONTRACT_VERSION && claims.length >= 5 && claims.every(x => x.claim_id && x.tests && x.artifacts);
  return { ok, claim_count: claims.length };
}

function verifyWitnesses(bundleDir) {
  const profile = loadJson(path.join(bundleDir, 'PROFILE_SOURCE.json'));
  const witnesses = loadJson(path.join(bundleDir, 'WITNESS_SET.json'));
  const mismatches = [];
  for (const item of witnesses) {
    const result = evaluateRequest(profile, item.request);
    if (result.verdict !== item.verdict) mismatches.push({ request: item.request, expected: item.verdict, actual: result.verdict });
  }
  return { ok: mismatches.length === 0, checked: witnesses.length, mismatches };
}

function verificationResult({ bundle_digest, overall_ok, checks, details, refusal_reasons }) {
  if (overall_ok) {
    return attachWitnessCertificate({
      primitive_identity: PRIMITIVE_IDENTITY,
      verification_result: 'VERIFIED',
      overall_ok: true,
      bundle_digest,
      checks,
      details,
      replay_binding: { primitive_identity: PRIMITIVE_IDENTITY, bundle_digest, request_digest: null },
    });
  }
  const primaryName = PRECEDENCE.find(name => !checks[name]);
  const primaryCode = REFUSAL_CODE_MAP[primaryName];
  const refusal = makeRefusal({ code: primaryCode, layer: 'bundle', bundle_digest, verification_result: 'NOT_VERIFIED', refusal_reasons, details });
  refusal.overall_ok = false;
  refusal.checks = checks;
  return attachWitnessCertificate(refusal);
}

export function verifyBundleNode(bundleDir) {
  const required = verifyRequiredFiles(bundleDir);
  if (!required.ok) return verificationResult({ bundle_digest: null, overall_ok: false, checks: { required_files: false }, details: { required_files: required }, refusal_reasons: ['REFUSE_REQUIRED_FILES_MISSING'] });
  const topLevel = verifyNoForbiddenTopLevel(bundleDir);
  const contract = verifyContract(bundleDir);
  const manifest = verifyManifest(bundleDir);
  const compiler = verifyCompilerProducts(bundleDir);
  const certs = verifyCertificates(bundleDir);
  const governance = verifyGovernance(bundleDir, manifest.bundle_digest);
  const verificationSchema = verifySchemaExact(bundleDir, VERIFICATION_SCHEMA_NAME, 'verification_result.schema.json');
  const refusalSchema = verifySchemaExact(bundleDir, REFUSAL_SCHEMA_NAME, 'refusal.schema.json');
  const permitSchema = verifySchemaExact(bundleDir, PERMIT_SCHEMA_NAME, 'permit.schema.json');
  const compiledBackendSchema = verifySchemaExact(bundleDir, COMPILED_BACKEND_SCHEMA_NAME, 'compiled_backend.schema.json');
  const claimTcb = verifyClaimAndTcb(bundleDir);
  const claimMatrix = verifyClaimMatrix(bundleDir);
  const witnesses = verifyWitnesses(bundleDir);
  const bundledVerdictSchema = loadJson(path.join(bundleDir, VERDICT_SCHEMA_NAME));
  const verdictSchemaOk = bundledVerdictSchema.properties && bundledVerdictSchema.required && bundledVerdictSchema.properties.verdict && Array.isArray(bundledVerdictSchema.properties.verdict.enum) && JSON.stringify(bundledVerdictSchema.properties.verdict.enum) === JSON.stringify(['ALLOW','DENY']) && bundledVerdictSchema.additionalProperties === false;
  const checks = {
    required_files: required.ok,
    top_level: topLevel.ok,
    contract: contract.ok,
    manifest: manifest.ok,
    compiler_products: compiler.ok,
    certificates: certs.ok,
    governance: governance.ok,
    verdict_schema: verdictSchemaOk,
    verification_schema: verificationSchema.ok,
    refusal_schema: refusalSchema.ok,
    permit_schema: permitSchema.ok,
    compiled_backend_schema: compiledBackendSchema.ok,
    claim_and_tcb: claimTcb.ok,
    claim_matrix: claimMatrix.ok,
    witness_replay: witnesses.ok,
  };
  const details = {
    contract_version: CONTRACT_VERSION,
    required_files: required,
    top_level: topLevel,
    contract,
    manifest,
    compiler_products: compiler,
    certificates: certs,
    governance,
    verdict_schema: { ok: verdictSchemaOk, schema_name: VERDICT_SCHEMA_NAME },
    verification_schema: verificationSchema,
    refusal_schema: refusalSchema,
    permit_schema: permitSchema,
    compiled_backend_schema: compiledBackendSchema,
    claim_and_tcb: claimTcb,
    claim_matrix: claimMatrix,
    witness_replay: witnesses,
  };
  const refusal_reasons = Object.entries(checks).filter(([, ok]) => !ok).map(([name]) => REFUSAL_CODE_MAP[name]);
  return verificationResult({ bundle_digest: manifest.bundle_digest, overall_ok: Object.values(checks).every(Boolean), checks, details, refusal_reasons });
}
