# ADEQUACY_MATRIX_TRUTH_SYNC_PASS

## Scope
This pass truth-synchronizes the adequacy matrix to the actually present release contents.

## Concrete corrections
- Upgraded `VF-07`, `VF-08`, `VF-09`, `VF-10`, `VF-12`, `VF-13`, and `VF-14` from `PARTIAL` to `FULL`.
- Rebound those rows to the present verification-subfamily adversarial corpus families and parity reports.
- Rewrote the residual-gap table so it no longer claims absent verification-subfamily corpus that already exists.
- Reduced `SPEC/ADEQUACY_RELEASE_POLICY.json` allowed partial rows to `C14N-06` and `EQ-07` only.
- Updated `SPEC/ADEQUACY_EXECUTABLE_CONTRACT.md` so its prose matches the corrected policy.
- Strengthened `tools/adequacy_matrix_gate.py` with stale-partial drift detection for verification-subfamily rows.
- Rebuilt `SPEC/ADEQUACY_MATRIX.json` from markdown after synchronization.
- Resynced the same adequacy spec files into `dist/standalone_verifier_release_root/SPEC/`.

## Remaining exact residual gaps
- `C14N-06`: canonicalization family breadth remains narrower than full object-family saturation.
- `EQ-07`: same-repository independent Python second-line parity remains useful but is not by itself an out-of-repository external line.
- Cross-repo parity remains contract-ready and gateable, but not yet fed by a physically separate externally hosted CI run.
- Theorem discharge remains executable-witness strong rather than theorem-prover/mechanized discharge.

## Gate result
- `dist/adequacy_matrix_gate_report.json` -> `overall_ok = true`

## Truthfulness effect
The adequacy matrix no longer understates verification-subfamily adversarial completion. The matrix, JSON mirror, release policy, and executable gate are now synchronized to the actual release contents for the corrected rows.
