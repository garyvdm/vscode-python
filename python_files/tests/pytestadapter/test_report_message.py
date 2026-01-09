from textwrap import indent

from _pytest.config import get_config
from _pytest.pytester import Pytester

from vscode_pytest import get_report_message


def test_report_message_failed_test(pytester: Pytester):
    # with suspend_capture(capsys):
    run = pytester.inline_runsource(
        """
        def test_function():
            print("stdout message")
            assert False, "Forced failure"
        """,
    )
    setup, call, teardown = run.getreports("pytest_runtest_logreport")

    config = get_config([])
    config.parse([], addopts=False)
    message = get_report_message(call, config)
    print(indent(message, "    "))

    message_lines = message.splitlines()

    assert message_lines[0] == "AssertionError: Forced failure - assert False", (
        "The first line should be a short summary of the failure."
    )
    assert "test_report_message_failed_test.py:3: AssertionError" in message_lines, (
        "Message should contain the traceback"
    )
    assert any("Captured stdout call" in line for line in message_lines), (
        "Message should contain the header for the stdout"
    )
    assert "stdout message", "Message should contain stdout"
