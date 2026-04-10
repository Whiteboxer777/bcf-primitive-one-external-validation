# RELEASE_SURFACE.md

## Purpose

This document defines the intended top-level release surface for the current internal RC source line.

It exists to keep the root of the artifact compact, auditable, and stable, while preserving historical pass-by-pass reports in `HISTORY/pass_reports/`.

## Canonical top-level documents

The current canonical top-level release surface is:

- `README.md`
- `RC_CLAIM_BOUNDARY.md`
- `RC_RESIDUAL_GAPS.md`
- `CLAIM.md`
- `LIMITS.md`
- `TCB.md`
- `VERIFIER_TCB.md`
- `REPRODUCE.md`
- `RELEASE_STATUS.md`
- `RELEASE_SURFACE.md`
- `pyproject.toml`

## Canonical directories

The current canonical top-level directories are:

- `SPEC/`
- `PROOFS/`
- `REPORTS/`
- `dist/`
- `schemas/`
- `src/`
- `tests/`
- `tools/`
- `corpus/`
- `externalized_second_line/`
- `node_second_line/`
- `repo_exports/`
- `mechanized_kernel/`
- `HISTORY/`

## Historical pass reports

Pass-specific narrative reports are retained under:

- `HISTORY/pass_reports/`

They are preserved for audit traceability but are not part of the compact canonical release surface.

## Root-level interpretation rule

The root of the artifact should not accumulate unbounded historical pass reports. Ongoing historical detail belongs in:

- `HISTORY/pass_reports/`
- `REPORTS/`
- `dist/`

This keeps the release surface minimal without deleting evidence.

## Canonical release refinement

See `SPEC/CANONICAL_TRUST_RELEASE.md` and `SPEC/TRUST_BOUNDARY_MATRIX.md` for the authoritative post-compression release surface.
