from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_duplicate_surface_gate() -> None:
    subprocess.run([sys.executable, 'tools/duplicate_surface_gate.py'], cwd=ROOT, check=True)
    report = json.loads((ROOT / 'dist' / 'duplicate_surface_gate_report.json').read_text(encoding='utf-8'))
    assert report['overall_ok'] is True
