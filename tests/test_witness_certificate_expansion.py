from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_witness_certificate_expansion_gate() -> None:
    subprocess.run([sys.executable, 'tools/witness_certificate_expansion_gate.py'], cwd=ROOT, check=True)
    report = json.loads((ROOT / 'dist/witness_certificate_expansion_report.json').read_text(encoding='utf-8'))
    assert report['overall_ok'] is True
    assert report['expanded_sample_artifacts_present'] is True
