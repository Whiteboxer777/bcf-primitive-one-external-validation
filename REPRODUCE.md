# Reproduce

## Local verification

```bash
pytest -q
python tools/run_one_shot_proof.py examples/canonical/invoice_profile.json examples/canonical/invoice_request_allow.json examples/canonical/invoice_deny_request.json
python tools/audit_bundle.py examples/canonical/invoice_profile.json examples/canonical/invoice_request_allow.json examples/canonical/invoice_deny_request.json
```

## Build standalone verifier release

```bash
python tools/build_standalone_verifier.py . dist/BCF_PRIMITIVE_ONE_STANDALONE_VERIFIER.zip
```
