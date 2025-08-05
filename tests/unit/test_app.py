from subprocess import CompletedProcess

from blueprint.cli import app as app_module
from blueprint.cli.app import App


def test_app():
    app = App()
    assert app


def test_app_system_user_git(subprocess_run_mock):
    """
    GIVEN: `git config --get user.name` returns a value
    AND:   `git config --get user.email` returns a value
    WHEN: app.system_user is accessed
    THEN: "name <email>" is returned
    """
    mock = subprocess_run_mock
    mock.rvs = ["Jane Doe", "jane.doe@fake.com"]

    mock.side_effect = lambda *a, **k: CompletedProcess(
        args=[],
        returncode=0,
        stdout=mock.rvs.pop(0),
    )

    app = App()
    user = app.system_user

    calls = mock.call_args_list

    assert len(calls) == 2
    assert user == "Jane Doe <jane.doe@fake.com>"


def test_app_system_user_getpass(subprocess_run_mock, monkeypatch):
    """
    GIVEN: `git config --get user.name` does not return a value
    AND:   `git config --get user.email` does not return a value
    AND: getpass.getuser() returns a value
    AND: socket.gethostname() returns a value
    WHEN: app.system_user is accessed
    THEN: "user <user@hostname>" is returned
    """
    with monkeypatch.context() as m:
        m.setattr(app_module.getpass, "getuser", lambda: "jane")
        m.setattr(app_module.socket, "gethostname", lambda: "fakehost")

        app = App()
        user = app.system_user

        assert user == "jane <jane@fakehost>"
