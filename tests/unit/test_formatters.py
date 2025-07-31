import pytest

from blueprint.formatters import (to_camel_case, to_kebab_case, to_pascal_case,
                                  to_smooshed_case, to_snake_case,
                                  to_title_case)


@pytest.mark.parametrize(["text", "expected"], [
    ["my project", "my_project"]
])
def test_to_snake_case(text, expected):
    assert to_snake_case(text) == expected


@pytest.mark.parametrize(["text", "expected"], [
    ["my project", "myProject"]
])
def test_to_camel_case(text, expected):
    assert to_camel_case(text) == expected


@pytest.mark.parametrize(["text", "expected"], [
    ["my project", "MyProject"]
])
def test_to_pascal_case(text, expected):
    assert to_pascal_case(text) == expected


@pytest.mark.parametrize(["text", "expected"], [
    ["my project", "my-project"]
])
def test_to_kebab(text, expected):
    assert to_kebab_case(text) == expected


@pytest.mark.parametrize(["text", "expected"], [
    ["my project", "myproject"]
])
def test_to_smooshed_case(text, expected):
    assert to_smooshed_case(text) == expected


@pytest.mark.parametrize(["text", "expected"], [
    ["my project", "My Project"]
])
def test_to_title_case(text, expected):
    assert to_title_case(text) == expected
