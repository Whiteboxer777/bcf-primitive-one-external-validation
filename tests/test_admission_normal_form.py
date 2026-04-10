
from tools.admission_normal_form_gate import main as run_gate
from bcf_primitive_verifier.common import load_json
from pathlib import Path


def test_admission_normal_form_gate():
    assert run_gate() == 0
    report = load_json(Path('dist/admission_normal_form_gate_report.json'))
    assert report['overall_ok'] is True
    assert all(row['overall_ok'] for row in report['profile_rows'])
