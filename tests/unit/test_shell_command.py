from os import environ
from pathlib import Path
from subprocess import CompletedProcess

import pytest

from blueprint.shell_command import ShellCommand
from tests.unit import cmd_strip_prefix

bp = breakpoint


def test_shell_command():
    cmd = ShellCommand()
    assert cmd


def test_shell_command_init():
    cmd = ShellCommand("python", "--version", encoding="utf8")

    assert cmd.program == "python"
    assert cmd.args == ("--version",)
    assert cmd.encoding == "utf8"


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


def test_shell_command_cwd():
    """
    GIVEN: A ShellCommand object with a ._cwd Path object
    WHEN:  .cwd is called
    THEN:  it should return a string
    """
    cmd = ShellCommand()
    cmd._cwd = Path.cwd()

    assert cmd.cwd == str(Path.cwd())


def test_shell_command_stdout():
    """
    GIVEN: A ShellCommand object
    WHEN:  the .stdout setter is used
    THEN:  .stdout should be set
    AND:   run_params.capture_output should be False
    """
    cmd = ShellCommand()
    cmd.stdout = True

    assert cmd.stdout is True
    assert cmd.capture_output is False


def test_shell_command_shell():
    """
    GIVEN: A ShellCommand object
    AND:   .shell is set to True
    WHEN:  .run() is called
    THEN:  the command sent to subprocess.run should be a string (not a list)
    """
    cmd = ShellCommand("ls")
    cmd.shell = True

    assert cmd.shell is True
    assert cmd_strip_prefix(cmd.run_cmd) == "ls"


def test_shell_command_exec(subprocess_run_mock):
    """
    GIVEN: A ShellCommand object
    WHEN:  .exec() is called
    THEN:  it should call subprocess.run()
    AND:   it should return a CompletedResult object
    AND:   .result should be set to the result
    """
    mock = subprocess_run_mock

    rv = CompletedProcess([], 0, stdout="hello", stderr="goodbye")
    mock.return_value = rv

    cmd = ShellCommand("ls")

    res = cmd.exec()

    try:
        call = mock.call_args_list[0]
    except BaseException:
        assert False, "Should have been called at least once."

    assert res == rv
    assert cmd.result == rv

    assert cmd_strip_prefix(call.args[0]) == ["ls"]


def test_shell_command_result():
    """
    GIVEN: A ShellCommand object
    WHEN:  the .result setter is used
    THEN:  .code should be set to the exit code
    AND:   .out should be set if present
    AND:   .err should be set if present
    """
    res = CompletedProcess([], 0, stdout="hello", stderr="goodbye")

    cmd = ShellCommand()
    cmd.result = res

    assert cmd.result == res
    assert cmd.code is res.returncode
    assert cmd.out is res.stdout
    assert cmd.err is res.stderr


def test_shell_command_run_cmd():
    """
    WHEN:  .run_cmd is accessed
    THEN:  it should return the command to send to subprocess.run()
           (the first argument)
    """
    cmd = ShellCommand("ls", "-l")
    assert cmd_strip_prefix(cmd.run_cmd) == ["ls", "-l"]


@pytest.mark.parametrize(["params", "expected", "given", "then"], [
    (
        {},
        dict(capture_output=True, text=True),
        "no object params",
        "return the default params",
    ),
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
def test_shell_command_run_kwargs(params, expected, given, then):
    """
    GIVEN: A ShellCommand object
    WHEN: .run_kwargs is accessed
    THEN: it should return a dict of kwargs to send to run
    """

    cmd = ShellCommand("pwd", **params)

    kwargs = cmd.run_kwargs
    kwargs.pop("env", None)

    assert kwargs == expected, (
        f"Given a ShellCommand object with {given}, "
        "when .run_kwargs is accessed, it should {then}."
    )


def test_shell_command__env():
    """
    WHEN:  A ShellCommand() object is initialzed with an env keyword
    THEN:  it should set ._env_
    """
    cmd = ShellCommand(env={"CLICOLOR": False})

    assert cmd._env == {"CLICOLOR": False}


def test_shell_command_env_not_empty():
    """
    GIVEN: A ShellCommand object with values in ._env
    WHEN:  the .env is accessed
    THEN:  it should return a dictionary that contains the values from os.environ
    AND:   the values from ._env
    AND:   the values from ._env should take precidence
    """
    cmd = ShellCommand()

    cmd._env["PYTHONPYCACHEPREFIX"] = "dot-pycache"

    assert cmd.env.get("PWD") == str(Path.cwd())
    assert cmd.env.get("PYTHONPYCACHEPREFIX") == "dot-pycache"


def test_shell_command_env_path():
    """
    GIVEN: A ShellCommand object
    WHEN:  the .env_path setter is used
    THEN:  PATH should be added to .env
    AND:   the path or paths should be prepended to os.environ["PATH"]
    AND:   .run_kwargs should include "PATH"
    """
    cmd = ShellCommand(env_path="./bin")
    old_path = environ.get("PATH", "")

    new_path = f"./bin:{old_path}"

    assert cmd.env_path == new_path
    assert cmd.env.get("PATH") == new_path
    assert cmd.run_kwargs.get("env", {}).get("PATH", "") == new_path


def test_shell_command_ok(subprocess_run_mock):
    """
    GIVEN: A command that reults in a non-zero exit status
    WHEN:  .exec() is called
    THEN:  .ok should be False
    """
    subprocess_run_mock.return_value = CompletedProcess([], 1, stderr="command failed")

    cmd = ShellCommand("xxx")
    cmd.exec()

    assert not cmd.ok()


def test_shell_command_():
    """
    GIVEN: ...
    WHEN:  ...
    THEN:  ...
    """
