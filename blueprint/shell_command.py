"""ShellCommand class."""

from os import environ
from shutil import which
from subprocess import CompletedProcess, run

from frozendict import frozendict

from blueprint.attr import attr, hasattrs
from blueprint.object import Object

bp = breakpoint


@hasattrs
class ShellCommand(Object):
    """Commands to run in shell."""

    capture_output: bool = True
    """Default capture_output value to send to subprocess.run()."""

    text: bool = True
    """Default text value to send to subprocess.run()."""

    code: int = None
    """Exit code."""

    res: CompletedProcess = None
    """Result object."""

    out: str = None
    """Result stdout."""

    err: str = None
    """Result stderr."""

    PARAMS: tuple = (
        "capture_output",
        "text",
        "cwd",
        "env",
    )
    """List of kwargs to send to subprocess.run() if present."""

    def __init__(self, program=None, *args, **kwargs):
        """Initialize the object.

        Args:
            program (str):  program to run
            *args (str): command line args

            **params:
                - env_path (str|list): a path or list of paths
                                       to prefix to env["PATH"]
                - subprocess.run()/Popen kwargs, including (but not limited to):
                    - shell (bool): shell mode
                    - capture_output (bool, default=True): capture
                                                           stdout/stderr
                    - text (bool, default=True): stdout/stderr in text mode
                    - cwd (path|str): working directory in which to run command
                    - stdout (PIPE|stream): where to direct stdout
                    - stderr (PIPE|stream): where to direct stderr
                    - env (dict): environment variables

        """
        self.program = program
        self.args = args

        self._env = kwargs.pop("env", {})
        self.env_path = kwargs.pop("env_path", [])

        self.kwargs = kwargs
        super().__init__(**kwargs)

    def __getattr__(self, name):
        """Return None if attribute is missing."""
        return None

    # subprocess.run() kwarg accessors {{{
    # ---------------------------------------------------------------------------

    @attr
    def cwd(self):
        """Access current working directory."""
        if not self._cwd:
            return

        return str(self._cwd)

    @attr(method="setter")
    def stdout(self, value):
        """Access stdout."""
        self._stdout = value
        if value:
            self.capture_output = False

    @property
    def env(self) -> frozendict:
        """Access env.

        If ._env is set, return os.environ combined with ._env.

        NOTE: Immutable, as values should be modified via ._env.
        """
        env = environ.copy()
        env.update(self._env)
        return frozendict(env)

    # ---------------------------------------------------------------------------
    # }}} / subprocess.run() kwarg accessors

    # attribute accessors {{{
    # ---------------------------------------------------------------------------

    @attr
    def env_path(self):
        """Get env_path.

        Return a string of the ._env_path list of paths then os.environ["PATH"]
        joined by ":".
        """
        if not self._env_path:
            return

        return ":".join([*self._env_path, environ.get("PATH", "")])

    @env_path.setter
    def env_path(self, paths):
        """Set env_paths.

        Set ._env_path to the list of paths, and set ._env["PATH"] to the
        modified path string (from .env_path).
        """
        if not paths:
            return
        if isinstance(paths, str):
            paths = [paths]
        self._env_path = paths
        self._env["PATH"] = self.env_path

    @property
    def which(self):
        """Return path to program."""
        return which(self.program)

    @property
    def run_cmd(self):
        """Get the command to send to subprocess.run()."""
        cmd = [self.which or self.program, *self.args]
        if self.shell:
            cmd = " ".join(cmd)
        return cmd

    @property
    def run_kwargs(self):
        """Return a dict of kwargs to pass to subprocess.run()."""
        kwargs = {}
        for key in [*self.PARAMS, *self.kwargs.keys()]:
            if key in kwargs:
                continue
            value = getattr(self, key, None)
            if value is not None:
                kwargs[key] = value
        return kwargs

    @attr(method="setter")
    def result(self, res) -> CompletedProcess:
        """Access result."""
        if not res:
            return
        if not isinstance(res, CompletedProcess):
            raise TypeError(
                "ShellCommand.result: must be a CompletedProcess, not {type(res)}"
            )
        self._result = res
        self.code = res.returncode
        self.out = res.stdout and res.stdout.strip() or None
        self.err = res.stderr

    # ---------------------------------------------------------------------------
    # }}} / attribute accessors

    # methods {{{
    # ---------------------------------------------------------------------------

    def exec(self) -> CompletedProcess:
        """Execute the command."""
        self.result = run(self.run_cmd, **self.run_kwargs)
        return self.result

    def ok(self) -> bool:
        """Check if result was successful."""
        if not self.result:
            return
        return self.code == 0

    # ---------------------------------------------------------------------------
    # }}} / methods
