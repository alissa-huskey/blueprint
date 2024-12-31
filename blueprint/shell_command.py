"""ShellCommand class."""

from shutil import which

from blueprint.object import Object

bp = breakpoint


class ShellCommand(Object):
    """Commands to run in shell."""

    DEFAULT_PARAMS = dict(
        capture_output=True,
        text=True,
    )

    _run_params: dict = {}

    def __init__(self, program=None, *args, **params):
        """Initialize the object.

        Args:
            program (str): shell program to run
            *args (str): command line args
            **params: subprocess.run() kewargs
        """
        self.program = program
        self.args = args
        self.run_params = params

    @property
    def run_params(self):
        """Get run_params."""
        params = self.DEFAULT_PARAMS.copy()
        params.update(self._run_params)
        return params

        return self._run_params

    @run_params.setter
    def run_params(self, value):
        """Set run_params."""
        self._run_params = value

    @property
    def which(self):
        """Return path to program."""
        return which(self.program)

    @property
    def command(self):
        """Return a list that contains program and all args."""
        if not self.program:
            return
        return [self.program, *self.args]
