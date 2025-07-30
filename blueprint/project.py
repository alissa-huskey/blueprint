"""Module for a Project."""

from pathlib import Path
from re import compile as re_compile
from string import Template as TemplateString
from subprocess import run

#  from blueprint import ROOT, AccessError, ProgramError
from blueprint import AccessError, ProgramError
from blueprint.attr import attr
from blueprint.object import Object
from blueprint.template import Template

bp = breakpoint


class Project(Object):
    """A new project."""

    pascal_replacer = re_compile(r'[-]([a-z])')
    smoosh_replacer = re_compile(r'[-_ ]')
    DEFAULT_VERSION = "0.0.1"

    _substitutions = {}

    def __init__(self,
                 template=None,
                 name=None,
                 dest=None,
                 summary="",
                 license="",
                 **kwargs):
        """Create a new project object."""
        self.template = template
        self.name = name
        self.dest = dest
        self.summary = summary or ""
        self.license = license or ""

        if self.template and self.template.specs:
            for key, value in (self.template.specs.get("options", {})).items():
                key = key.replace("-", "_")
                setattr(self, key, kwargs.pop(key, value.get("default", "")))

        super().__init__(**kwargs)

    @attr(method="setter")
    def template(self, value) -> Template:
        """Set the template."""
        if isinstance(value, str):
            value = Template(value)
        self._template = value

    @attr(method="setter")
    def dest(self, value) -> Path:
        """Define self.dest property.

        Validates and sets dest.
        """
        if not value:
            return

        dest = Path(value)
        if not dest.is_dir():
            raise AccessError(f"Cannot create project in: '{dest}'")

        self._dest = dest

    @property
    def path(self) -> Path:
        """Path to the project directory."""
        if not self.dest:
            return None
        return self.dest / self.dash_name

    @property
    def pascal_name(self) -> str:
        """Return the pascal version of the project name.

        Example: MyProject
        """
        return self.title_name.replace(" ", "")

    @property
    def dash_name(self) -> str:
        """Return the dash version of the project name.

        Example: my-project
        """
        return self.name.lower().translate(str.maketrans("_ ", "--"))

    @property
    def snake_name(self) -> str:
        """Return the snake tail version of the project name.

        Example: my_project
        """
        return self.name.lower().translate(str.maketrans("- ", "__"))

    @property
    def smooshed_name(self) -> str:
        """Return the snake tail version of the project name.

        Example: my_project
        """
        return self.smoosh_replacer.sub("", self.name.lower())

    @property
    def title_name(self) -> str:
        """Return the title case version of the project name.

        Example: My Project
        """
        return self.name.translate(str.maketrans("-_", "  ")).title()

    def create(self):
        """Create the project."""
        self.path.mkdir(exist_ok=True)

    def install(self, path, template=None):
        """Copy a file or create an empty directory from the source to the dest."""
        template = template or self.template

        if isinstance(path, str):
            path = template.skeleton / path

        rel_path = Path(*[
            self.substitute(p)
            for p in path.relative_to(template.skeleton).parts
        ])

        dest = self.path / rel_path

        dest.parent.mkdir(parents=True, exist_ok=True)

        if path.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
            return

        src_text = path.read_text()
        text = self.substitute(src_text)
        dest.write_text(text)

    @property
    def substitutions(self):
        """Return a mapping of the file substitutions for installing files."""
        if not self._substitutions:
            self._substitutions = {
                "DASH_NAME": self.dash_name,
                "TITLE_NAME": self.title_name,
                "SNAKE_NAME": self.snake_name,
                "SMOOSHED_NAME": self.smooshed_name,
                "PASCAL_NAME": self.pascal_name,
                "VERSION": self.DEFAULT_VERSION,
                "SUMMARY": self.summary,
                "LICENSE": self.license,
                "TEMPLATE_ROOT": (self.template and self.template.root or ""),
                "DEST": self.dest,
                "PATH": self.path,
            }

            if self.template:
                # set the options defined in blueprint.json
                for key in (self.template.options or {}):
                    name = key.translate(str.maketrans("- ", "__"))
                    self._substitutions[name.upper()] = getattr(self, name, "")

                # set the arguments defined in blueprint.json
                for key in (self.template.arguments or {}):
                    name = key.translate(str.maketrans("- ", "__"))
                    self._substitutions[name.upper()] = getattr(self, name, "")

                extra = {}
                # set the variables defined in blueprint.json
                for key, exe in (self.template.variables or {}).items():
                    name = key.translate(str.maketrans("- ", "__"))

                    # don't use self.run(..., substitute=True)
                    # to avoid infinite recursion
                    cmd = [self.substitute(x, self._substitutions) for x in exe["cmd"]]

                    res = self.run(cmd)
                    if res.stdout:
                        extra[key] = res.stdout.strip()
                self._substitutions.update(extra)

        return self._substitutions

    def substitute(self, text, variables=None) -> str:
        """Replace all substitutions with their variables."""
        variables = variables or self.substitutions
        return TemplateString(text).safe_substitute(**variables)

    def install_all(self, template=None):
        """Install all dotfiles from sources into the new project directory."""
        template = template or self.template

        if template.parent:
            self.install_all(template.parent)

        for path in template.skeleton.glob("**/*"):
            self.install(path, template)

    def run(
        self,
        command: list,
        substitute=False,
        options=None,
        capture_output=True,
        text=True,
        **kwargs
    ):
        """Run a CLI command.

        Args:
            * command (list): command to run
            * substitute (bool, default=False): replace template variables in command?
            * options (dict, default=None): maps template variable -> list of arguments
                                            if template variable is present
                                            add list of arguments after substitution
            * capture_output (bool, default=True): if output should be captured
            * text (bool, default=True): decode text in output?
            * shell (bool, default=False): run in shell mode
                                           sends command as joined string
            * **kwargs: arguments to forward to subprocess.run
        """
        cwd = kwargs.pop("cwd", self.path)

        if substitute:
            command = [self.substitute(x) for x in command]

        for key, args in (options or {}).items():
            if (self.substitute(key)):
                command.extend([self.substitute(arg) for arg in args])

        if kwargs.get("stdout"):
            capture_output = False

        params = dict(
            capture_output=capture_output,
            text=text,
        )

        if cwd:
            params["cwd"] = str(cwd)

        params.update(kwargs)

        # if keyword arg shell=True is passed to run()
        # the command must be a simple string
        if params.get("shell"):
            command = " ".join(command)

        res = run(command, **params)

        if res.returncode:
            cmd = " ".join(command)
            err = ""
            if hasattr(res, "stderr"):
                err = res.stderr
            raise ProgramError(
                f"Failed CLI command [{res.returncode}] {cmd!r}: {err!r}"
            )

        return res

    def add_dependencies(self):
        """Install all dependencies from the config file."""
        if not (
            (cmds := self.template.specs.get("dependency-commands"))
            and self.template.config
            and self.template.config.exists()
            and self.template.config.read()
            and (cfg := self.template.config.dependencies)
        ):
            return

        for key in ["main", "dev"]:
            if ((cmd := cmds.get(key)) and (deps := cfg.get(key))):
                for dep in deps:
                    c = cmd.copy()
                    c.append(dep)
                    self.run(c)

    def setup(self, template=None):
        """Execute setup steps."""
        template = template or self.template

        if template.parent:
            self.setup(template.parent)

        for step in (template.setup or []):
            cmd = step["cmd"]
            outfile = step.get("out")
            params = {"substitute": True, "options": step.get("options", {})}
            if outfile:
                path = self.path / outfile
                with open(path, "w") as fp:
                    self.run(cmd, stdout=fp, **params)
            else:
                self.run(cmd, **params)

    def make(self):
        """Make the project end-to-end."""
        self.create()
        self.setup()
        self.install_all()
        self.add_dependencies()
