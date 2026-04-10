from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_object_canonicalization_impossibility_saturation_gate() -> None:
    subprocess.run([sys.executable, 'tools/object_canonicalization_impossibility_saturation_gate.py'], cwd=ROOT, check=True)
    report = json.loads((ROOT / 'dist/object_canonicalization_impossibility_saturation_report.json').read_text(encoding='utf-8'))
    assert report['overall_ok'] is True
    assert report['families']['object_model']['overall_ok'] is True
    assert report['families']['canonicalization']['overall_ok'] is True
    assert report['families']['impossibility']['overall_ok'] is True
