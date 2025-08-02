"""Blueprint tests."""

import json
from contextlib import contextmanager
from pathlib import Path
from re import compile as re_compile

from blueprint.config import Config
from blueprint.plan import Plan
from blueprint.schema import Schema

bp = breakpoint


stripper = re_compile(r'.*/')


def make_blueprint(
    path: Path,
    name: str,
    specs: str | dict | bool = None,
    files: dict = None
) -> Path:
    """Create a blueprint directory.

    Args:
        path (Path): Plans root directory
        name (str): Name of plan
        specs (str|dict|bool): blueprint.json contents or False to not create
        files (dict, default=None): files to create
                                    (file path (str) ->
                                        contents (str)
                                        or dir to create dir
                                    )

    Returns:
        (Path) Path to plan directory
    """
    files = files or {}

    plan_dir = path / name
    specs_file = plan_dir / "blueprint.json"

    plan_dir.mkdir(parents=True)

    if specs is not False:
        if isinstance(specs, dict):
            specs = json.dumps(specs)

        specs = specs or {}
        specs_file.write_text(specs)

    for file, contents in files.items():
        p = plan_dir / file

        if contents == dir:
            p.mkdir(parents=True, exist_ok=True)
            continue

        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(contents)
    return plan_dir


def cmd_strip_prefix(cmd: list | str) -> list | str:
    """Strip the full path from the program in a command list.

    Examples:
        >>> cmd_strip_prefix(['/opt/homebrew/opt/coreutils/libexec/gnubin/ls', "-l"])
        ['ls', '-l']
    """
    if not cmd:
        return cmd

    if isinstance(cmd, str):
        cmd = stripper.sub("", cmd)
    elif isinstance(cmd, list):
        cmd[0] = stripper.sub("", cmd[0])
    else:
        raise ValueError("cmd_strip_prefix(): cmd must be a list or string")
    return cmd


@contextmanager
def set_plans_root(root):
    """Temporarily modify the Plan.ROOT directory of a Project class."""
    orig = Plan.ROOT
    Plan.ROOT = root
    yield
    Plan.ROOT = orig


@contextmanager
def set_schemas_root(root):
    """Temporarily modify the Schema.ROOT path."""
    orig = Schema.ROOT
    Schema.ROOT = root
    yield
    Schema.ROOT = orig


@contextmanager
def set_config_base(base):
    """Temporarily modify the BASE directory of a Project class."""
    orig = Config.BASE
    Config.BASE = base
    yield
    Config.BASE = orig
