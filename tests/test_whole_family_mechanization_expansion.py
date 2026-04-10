from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_whole_family_mechanization_expansion_gate() -> None:
    subprocess.run(['python3', str(ROOT / 'tools' / 'whole_family_mechanization_expansion_gate.py')], check=True)
    report = json.loads((ROOT / 'dist' / 'whole_family_mechanization_expansion_report.json').read_text(encoding='utf-8'))
    assert report['overall_ok'] is True
    assert report['truth_boundary']['status_label'] == 'executable_witness_whole_family_mechanization_expansion'
    assert report['supporting_reports']['mechanized_kernel']['overall_ok'] is True
    assert report['supporting_reports']['admission_normal_form']['overall_ok'] is True
    assert report['supporting_reports']['compiled_backend']['overall_ok'] is True
    assert report['supporting_reports']['witness_certificate']['overall_ok'] is True
