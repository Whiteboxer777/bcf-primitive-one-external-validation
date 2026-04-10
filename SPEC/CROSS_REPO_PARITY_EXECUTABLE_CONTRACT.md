# `SPEC/CROSS_REPO_PARITY_EXECUTABLE_CONTRACT.md`

## 0. Status

This document is the executable-contract specification for cross-repo parity **preparation** of the out-of-family Node second line.

Its function is to bind exported-repo parity preparation to a machine-readable contract, CI workflow templates, executable gate scripts, and report artifacts so that cross-repo parity is not merely asserted but mechanically checked **at the export-prepared artifact boundary**.

The cross-repo parity executable-contract surface consists exactly of:

- `CI/CROSS_REPO_PARITY_CONTRACT.json`
- `tools/cross_repo_parity_ci_gate.py`
- `REPORTS/cross_repo_parity_ci_gate_report.json`
- `dist/cross_repo_parity_ci_gate_report.json`
- `repo_exports/node_second_line_repo/.github/workflows/node-second-line-parity-gate.yml`
- `repo_exports/node_second_line_repo/.github/workflows/node-second-line-cross-repo-artifact.yml`

## 1. Canonical rule

Cross-repo parity is satisfied only if the exported Node second-line repository can independently emit its self-check and theorem-discharge reports and those reports can be ingested by the main-line gate together with the main-line Node parity reports under the machine-readable parity contract.

## 2. Required parity dimensions

The parity contract requires exact checking of at least:

- verification parity
- runtime allow parity
- runtime refusal parity
- replay allow parity
- replay refusal parity
- primitive identity match
- theorem-discharge gate success in the exported repo

## 3. Required artifact inputs

The gate must consume the following report artifacts:

- main-line `REPORTS/node_out_of_family_parity_report.json`
- main-line `REPORTS/node_verification_subfamily_parity_report.json`
- exported-repo `reports/node_self_check_report.json`
- exported-repo `reports/node_theorem_discharge_report.json`

## 4. Output artifact

The executable gate must emit:

- `REPORTS/cross_repo_parity_ci_gate_report.json`
- `dist/cross_repo_parity_ci_gate_report.json`

These are the inspectable machine-audit artifacts for cross-repo parity CI contract conformance.
