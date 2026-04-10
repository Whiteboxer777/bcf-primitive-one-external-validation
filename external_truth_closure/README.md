# External Truth Closure

This surface is the clean-room rerun entrypoint for the canonical minimal trust release.

Authoritative entrypoint:

```bash
PYTHONPATH=src PYTHONDONTWRITEBYTECODE=1 python external_truth_closure/run_external_truth_closure.py
```

The rerun must emit:

- `dist/EXTERNAL_TRUTH_CHAIN.json`
- `dist/EXTERNAL_TRUTH_VERDICT.json`
- `dist/external_digest_reconciliation_report.json`

Required closure checks:

1. official verification route
2. one-shot proof route
3. external audit route
4. primary vs independent parity
5. primary vs node out-of-family parity
6. digest reconciliation across surfaces
7. artifact hygiene gate on the final release tree
