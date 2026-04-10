from mechanized_kernel.checker import run_mechanized_kernel_check


def test_mechanized_kernel_gate_report_ok():
    report = run_mechanized_kernel_check()
    assert report['overall_ok'] is True
    assert report['counters']['states_checked'] == 4096
    assert report['counters']['allow_states'] == 1
    assert report['counters']['refusal_states'] == 4095
