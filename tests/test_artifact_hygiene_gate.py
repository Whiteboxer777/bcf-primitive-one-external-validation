from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_artifact_hygiene_gate() -> None:
    # Factory-clean first: remove __pycache__, .pytest_cache, .pyc files
    # These are dev runtime artifacts that must not be present in a clean release
    subprocess.run([sys.executable, 'tools/artifact_hygiene_factory_clean.py'], cwd=ROOT, check=True)
    subprocess.run([sys.executable, 'tools/artifact_hygiene_gate.py'], cwd=ROOT, check=True)
    report = json.loads((ROOT / 'dist' / 'artifact_hygiene_gate_report.json').read_text(encoding='utf-8'))
    assert report['overall_ok'] is True
