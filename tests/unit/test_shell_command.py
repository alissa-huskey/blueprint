import pytest

from blueprint.shell_command import ShellCommand

bp = breakpoint


def test_shell_command():
    cmd = ShellCommand()
    assert cmd


def test_shell_command_init():
    cmd = ShellCommand("python", "--version", encoding="utf8")

    assert cmd.program == "python"
    assert cmd.args == ("--version",)
    assert isinstance(cmd.run_params, dict)
    assert "encoding" in cmd.run_params


@pytest.mark.parametrize(["program", "path", "given", "then"], [
    ("sh", "/bin/sh", "a program that is installed", "the path to the program"),
    ("xxx", None, "a program that is not installed", "None"),
])
def test_shell_command_which(program, path, given, then):
    """
    GIVEN: A ShellCommand object
    WHEN: .which is accessed
    THEN: It should return the path to the program or None.
    """
    cmd = ShellCommand(program)
    assert cmd.which == path, f"Given {given} ShellCommand.which should return {then}."


def test_shell_command_command():
    """
    GIVEN: A ShellCommand object with a command
    WHEN: .command is accessed
    THEN: it should return a list that contains the program and all args
    """
    cmd = ShellCommand("python", "--version")

    assert cmd.command == ["python", "--version"]


@pytest.mark.parametrize(["params", "expected", "given", "then"], [
    ({}, ShellCommand.DEFAULT_PARAMS, "no object params", "return the default params"),
    (
        dict(encoding="utf8"),
        {"capture_output": True, "text": True, "encoding": "utf8"},
        "params not in default",
        "return a dict that includes the object params",
    ),
    (
        dict(text=False),
        dict(capture_output=True, text=False),
        "an object param in the defaults with a different value",
        "override the default value"
    ),
])
def test_shell_command_params(params, expected, given, then):
    """
    GIVEN: A ShellCommand object
    WHEN: .run_params is accessed
    THEN: it should return a list of default params + object params
    AND: object params should override default params if present
    """

    cmd = ShellCommand("pwd", **params)

    assert cmd.run_params == expected, (
        f"Given a ShellCommand object with {given}, "
        "when .run_params is accessed it should {then}."
    )


def test_shell_command_():
    """
    GIVEN: ...
    WHEN: ...
    THEN: ...
    """
