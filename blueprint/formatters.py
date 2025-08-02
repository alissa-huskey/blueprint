"""String formatting functions."""

from os import environ
from pathlib import Path
from re import compile as re_compile

bp = breakpoint

pascal_replacer = re_compile(r'[-]([a-z])')
smoosh_replacer = re_compile(r'[-_ ]')

path_replacers = {
    Path.cwd(): ".",
    Path.home(): "~",
}

if (tmpdir := environ.get("TMPDIR")):
    path_replacers[Path(tmpdir)] = "$TMPDIR"


def to_title_case(text: str) -> str:
    """Convert text to Title Case."""
    return text.translate(str.maketrans("-_", "  ")).title()


def to_snake_case(text: str) -> str:
    """Convert text to snake_case."""
    return text.lower().translate(str.maketrans("- ", "__"))


def to_kebab_case(text: str) -> str:
    """Convert text to kebab-case."""
    return text.lower().translate(str.maketrans("_ ", "--"))


def to_pascal_case(text: str) -> str:
    """Convert text to PascalCase."""
    return to_title_case(text).replace(" ", "")


def to_camel_case(text: str) -> str:
    """Convert text to camelCase."""
    text = to_pascal_case(text)
    return f"{text[0].lower()}{text[1:]}"


def to_smooshed_case(text: str) -> str:
    """Convert text to smooshedcase."""
    return smoosh_replacer.sub("", text.lower())


def ppath(path: str | Path) -> str:
    """Pretty path.

    Replace home, cwd and tmppath with their shortened versions.
    """
    if isinstance(path, str):
        path = Path(path)

    for p, text in path_replacers.items():
        if path.is_relative_to(p):
            relpath = path.relative_to(p)
            return f"{text}/{relpath}"
    return str(path)
