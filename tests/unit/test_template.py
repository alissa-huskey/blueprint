from blueprint.template import Template


def test_template():
    tpl = Template()

    assert isinstance(tpl, Template)


def test_template_jinja():
    tpl = Template()

    assert "to_camel_case" in tpl._jinja.filters


def test_template_render():
    tpl = Template("{{ SMOOSHED_NAME }}", SMOOSHED_NAME="myproject")
    text = tpl.render()

    assert text == "myproject"


def test_template_():
    """
    GIVEN: ...
    WHEN:  ...
    THEN:  ...
    """
