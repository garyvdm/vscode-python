import _pytest.config
import pytest

from vscode_pytest import get_report_message


def test_1():
    args = []
    config = _pytest.config.get_config(args)
    config.parse(args, addopts=False)

    exception = None
    try:
        assert False
    except Exception as e:
        exception = e

    report = pytest.TestReport(
        "fake_test",
        ("fake_test.py", 1, "fake_test"),
        {},
        "failed",
        exception,
        "call",
    )
    report.sections.append(("Captured stdout", "stdout message"))
    print(get_report_message(report, config))
