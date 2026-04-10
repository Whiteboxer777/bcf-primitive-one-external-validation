from __future__ import annotations

from pathlib import Path

from tools.witness_certificate_gate import run_witness_certificate_gate


def test_witness_certificate_gate() -> None:
    root = Path(__file__).resolve().parents[1]
    report = run_witness_certificate_gate(root, root / 'examples' / 'canonical' / 'invoice_profile.json')
    assert report['overall_ok'] is True
    assert report['verification']['ok'] is True
    assert report['permit']['ok'] is True
    assert report['refusal']['ok'] is True
    assert report['replay_refusal']['ok'] is True
