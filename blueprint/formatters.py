"""String formatting functions."""

from re import compile as re_compile

pascal_replacer = re_compile(r'[-]([a-z])')
smoosh_replacer = re_compile(r'[-_ ]')


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
