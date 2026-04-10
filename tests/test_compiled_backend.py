from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'dist' / 'compiled_backend_gate_report.json'


def test_compiled_backend_gate() -> None:
    subprocess.run([sys.executable, 'tools/compiled_backend_gate.py'], cwd=ROOT, check=True)
    payload = json.loads(REPORT.read_text())
    assert payload['overall_ok'] is True
    assert payload['bundle_details']['overall_ok'] is True
    assert all(row['overall_ok'] for row in payload['profile_rows'])
