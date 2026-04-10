# STANDALONE_RELEASE_TRUTH_SYNC_PASS

Completed.

- Synced `dist/standalone_verifier_release_root/SPEC/` to the full current top-level `SPEC/` family.
- Synced top-level `PROOFS/` markdown/json into the standalone release root.
- Updated `src/bcf_primitive/capsule.py` so future standalone builds copy the full current `SPEC/` and `PROOFS/` trees, rather than a stale subset.
- Regenerated `dist/standalone_verifier_release.zip` and `dist/BCF_PRIMITIVE_ONE_STANDALONE_VERIFIER.zip`.
- Removed cache and temporary directories before packaging.
