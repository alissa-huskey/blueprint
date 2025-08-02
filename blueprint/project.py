"""Module for a Project."""

from pathlib import Path

from blueprint import AccessError, ProgramError
from blueprint.attr import attr
from blueprint.formatters import (to_kebab_case, to_pascal_case,
                                  to_smooshed_case, to_snake_case,
                                  to_title_case)
from blueprint.object import Object
from blueprint.plan import Plan
from blueprint.shell_command import ShellCommand
from blueprint.template import Template

bp = breakpoint


class Project(Object):
    """A new project."""

    _NO_REPR = ["_specs", "_dest"]

    DEFAULT_VERSION = "0.1.0"

    _substitutions = {}

    def __init__(self,
                 plan=None,
                 name=None,
                 dest=None,
                 summary="",
                 license="",
                 **kwargs):
        """Create a new project object."""
        self.plan = plan
        self.name = name
        self.dest = dest
        self.summary = summary or ""
        self.license = license or ""

        if self.plan and self.plan.specs:
            for key, value in (self.plan.specs.get("options", {})).items():
                key = key.replace("-", "_")
                setattr(self, key, kwargs.pop(key, value.get("default", "")))

        super().__init__(**kwargs)

    @attr(method="setter")
    def plan(self, value) -> Plan:
        """Set the plan."""
        if isinstance(value, str):
            value = Plan(value)
        self._plan = value

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

        name = self.dash_name

        if self.plan and self.plan.specs and self.plan.specs.get("project-dir"):
            name = self.substitute(self.plan.project_dir, variables={"NAME": self.name})

        return self.dest / name

    @property
    def pascal_name(self) -> str:
        """Return the pascal version of the project name.

        Example: MyProject
        """
        return to_pascal_case(self.title_name)

    @property
    def dash_name(self) -> str:
        """Return the dash version of the project name.

        Example: my-project
        """
        return to_kebab_case(self.name)

    @property
    def snake_name(self) -> str:
        """Return the snake tail version of the project name.

        Example: my_project
        """
        return to_snake_case(self.name)

    @property
    def smooshed_name(self) -> str:
        """Return the snake tail version of the project name.

        Example: my_project
        """
        return to_smooshed_case(self.name)

    @property
    def title_name(self) -> str:
        """Return the title case version of the project name.

        Example: My Project
        """
        return to_title_case(self.name)

    def create(self):
        """Create the project."""
        self.path.mkdir(exist_ok=True)

    def install(self, path, plan=None):
        """Copy a file or create an empty directory from the source to the dest."""
        plan = plan or self.plan

        if isinstance(path, str):
            path = plan.skeleton / path

        rel_path = path.relative_to(plan.skeleton)

        dest = self.path / self.substitute(str(rel_path))

        dest.parent.mkdir(parents=True, exist_ok=True)

        if path.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
            return

        text = plan.jinja.render(file=str(rel_path), **self.substitutions)
        dest.write_text(text)

    @property
    def substitutions(self):
        """Return a mapping of the file substitutions for installing files."""
        if not self._substitutions:
            self._substitutions = {
                "NAME": self.name,
                "DASH_NAME": self.dash_name,
                "TITLE_NAME": self.title_name,
                "SNAKE_NAME": self.snake_name,
                "SMOOSHED_NAME": self.smooshed_name,
                "PASCAL_NAME": self.pascal_name,
                "VERSION": self.DEFAULT_VERSION,
                "SUMMARY": self.summary,
                "LICENSE": self.license,
                "PLANS_ROOT": (self.plan and self.plan.root or ""),
                "DEST": self.dest,
                "PATH": self.path,
            }

            if self.plan:
                # set the options defined in blueprint.json
                for key in (self.plan.options or {}):
                    name = key.translate(str.maketrans("- ", "__"))
                    self._substitutions[name.upper()] = getattr(self, name, "")

                # set the arguments defined in blueprint.json
                for key in (self.plan.arguments or {}):
                    name = key.translate(str.maketrans("- ", "__"))
                    self._substitutions[name.upper()] = getattr(self, name, "")

                extra = {}
                # set the variables defined in blueprint.json
                for key, exe in (self.plan.variables or {}).items():
                    name = key.translate(str.maketrans("- ", "__"))

                    # don't use self.run(..., substitute=True)
                    # to avoid infinite recursion
                    cmd = [self.substitute(x, self._substitutions) for x in exe["cmd"]]

                    res = self.run(cmd)
                    if res.stdout:
                        extra[key] = res.stdout.strip()
                self._substitutions.update(extra)

        return self._substitutions

    def substitute(self, text, variables: dict = None) -> str:
        """Replace all substitutions with their variable values."""
        variables = variables or self.substitutions

        if self.plan and self.plan.jinja:
            return self.plan.jinja.render(text, **variables)
        else:
            return Template(text, **variables).render()

    def install_all(self, plan=None):
        """Install all dotfiles from sources into the new project directory."""
        plan = plan or self.plan

        if plan.parent:
            self.install_all(plan.parent)

        for path in plan.skeleton.glob("**/*"):
            self.install(path, plan)

    def run(
        self,
        command: list,
        substitute=False,
        options=None,
        **kwargs
    ):
        """Run a CLI command.

        Args:
            * command (list): command to run
            * substitute (bool, default=False): replace plan variables in command?
            * options (dict, default=None): maps plan variable -> list of arguments
                                            if plan variable is present
                                            add list of arguments after substitution
            * **kwargs: keyword arguments to forward to ShellCommand()
        """
        if substitute:
            command = [self.substitute(x) for x in command]

        for key, args in (options or {}).items():
            if (self.substitute(key)):
                command.extend([self.substitute(arg) for arg in args])

        cmd = ShellCommand(*command, cwd=kwargs.pop("cwd", self.path), **kwargs)
        res = cmd.exec()

        if not cmd.ok():
            raise ProgramError(
                f"Failed CLI command [{res.code}] {cmd!r}: {res.err!r}"
            )

        return res

    def add_dependencies(self):
        """Install all dependencies from the config file."""
        if not (
            (cmds := self.plan.specs.get("dependency-commands"))
            and self.plan.config
            and self.plan.config.exists()
            and self.plan.config.read()
            and (cfg := self.plan.config.dependencies)
        ):
            return

        for key in ["main", "dev"]:
            if ((cmd := cmds.get(key)) and (deps := cfg.get(key))):
                for dep in deps:
                    c = cmd.copy()
                    c.append(dep)
                    self.run(c)

    def setup(self, plan=None, steps="setup"):
        """Execute setup steps."""
        plan = plan or self.plan

        if plan.parent:
            self.setup(plan.parent, steps=steps)

        for step in plan.specs.get(steps, []):
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
        self.setup(steps="after")
