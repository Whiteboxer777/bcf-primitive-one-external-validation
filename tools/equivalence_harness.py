from __future__ import annotations

from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import json
from bcf_primitive.common import canonical_bytes, digest_data
from bcf_primitive.compiler import compile_bundle
from bcf_primitive.runtime import SealedBoundaryRunner
from bcf_primitive_verifier.runtime import replay_verdict
from bcf_primitive_verifier.verifier import verify_bundle
from tools.schema_validation_harness import run_schema_validation_harness
from tools.second_surface_parity_target import run_second_surface_parity_target
from tools.independent_second_implementation_parity import run_independent_second_implementation_parity
from tools.theorem_family_corpus_harness import run_theorem_family_corpus_harness
from tools.adversarial_closure_harness import run_adversarial_closure_harness
from tools.verification_subfamily_completion_harness import run_verification_subfamily_completion_harness
from tools.externalized_second_line_parity import run_externalized_second_line_parity
from tools.node_out_of_family_parity import run_node_out_of_family_parity
from tools.node_verification_subfamily_parity import run_node_verification_subfamily_parity


def run_equivalence_harness(project_root: str | Path, profile: str | Path) -> dict[str, object]:
    project_root = Path(project_root)
    profile = Path(profile)
    bundle = project_root / '.equivalence_bundle_tmp'
    if bundle.exists():
        import shutil
        shutil.rmtree(bundle)
    compile_bundle(profile, bundle)
    verify_report = verify_bundle(bundle)
    corpus = project_root / 'corpus' / 'canonicalization'
    req_a = json.loads((corpus / 'request_semantically_equal_a.json').read_text(encoding='utf-8'))
    req_b = json.loads((corpus / 'request_semantically_equal_b.json').read_text(encoding='utf-8'))
    req_distinct = json.loads((corpus / 'request_distinct.json').read_text(encoding='utf-8'))
    canon_a = canonical_bytes(req_a)
    canon_b = canonical_bytes(req_b)
    canon_distinct = canonical_bytes(req_distinct)
    replay_a = replay_verdict(bundle, req_a)
    replay_b = replay_verdict(bundle, req_b)
    replay_distinct = replay_verdict(bundle, req_distinct)
    runner = SealedBoundaryRunner(bundle)
    permit_a = runner.execute(req_a, {'action_id': 'eq-a', 'kind': 'emit', 'payload': {}})
    permit_b = runner.execute(req_b, {'action_id': 'eq-b', 'kind': 'emit', 'payload': {}})
    schema_report = run_schema_validation_harness(project_root, profile)
    second_surface = run_second_surface_parity_target(project_root, profile)
    independent_parity = run_independent_second_implementation_parity(project_root, profile)
    theorem_family = run_theorem_family_corpus_harness(project_root, profile)
    adversarial = run_adversarial_closure_harness(project_root, profile)
    verification_subfamily = run_verification_subfamily_completion_harness(project_root, profile)
    externalized_parity = run_externalized_second_line_parity(project_root, profile)
    node_out_of_family = run_node_out_of_family_parity(project_root, profile)
    node_verification_subfamily = run_node_verification_subfamily_parity(project_root, profile)
    overall_ok = bool(
        verify_report.get('overall_ok')
        and canon_a == canon_b
        and canon_a != canon_distinct
        and digest_data(req_a) == digest_data(req_b)
        and replay_a.get('verdict') == replay_b.get('verdict') == 'ALLOW'
        and replay_distinct.get('verdict') == 'ALLOW'
        and permit_a.get('verdict') == permit_b.get('verdict') == 'ALLOW'
        and permit_a.get('permit_binding', {}).get('bundle_digest') == permit_b.get('permit_binding', {}).get('bundle_digest')
        and permit_a.get('replay_binding', {}).get('request_digest') == permit_b.get('replay_binding', {}).get('request_digest')
        and schema_report.get('overall_ok')
        and second_surface.get('overall_ok')
        and independent_parity.get('overall_ok')
        and theorem_family.get('overall_ok')
        and adversarial.get('overall_ok')
        and verification_subfamily.get('overall_ok')
        and externalized_parity.get('overall_ok')
        and node_out_of_family.get('overall_ok')
        and node_verification_subfamily.get('overall_ok')
    )
    report = {
        'overall_ok': overall_ok,
        'verify_report': verify_report,
        'canonicalization': {
            'equal_a_b': canon_a == canon_b,
            'distinct_a_distinct': canon_a != canon_distinct,
            'digest_equal_a_b': digest_data(req_a) == digest_data(req_b),
        },
        'replay': {'a': replay_a, 'b': replay_b, 'distinct': replay_distinct},
        'permits': {'a': permit_a, 'b': permit_b},
        'schema_validation': schema_report,
        'second_surface_parity': second_surface,
        'independent_second_implementation_parity': independent_parity,
        'theorem_family_corpus': theorem_family,
        'adversarial_closure': adversarial,
        'verification_subfamily_completion': verification_subfamily,
        'externalized_second_line_parity': externalized_parity,
        'node_out_of_family_parity': node_out_of_family,
        'node_verification_subfamily_parity': node_verification_subfamily,
    }
    import shutil
    shutil.rmtree(bundle)
    return report


if __name__ == '__main__':
    print(json.dumps(run_equivalence_harness(ROOT, ROOT / 'examples' / 'canonical' / 'invoice_profile.json'), indent=2, sort_keys=True))
