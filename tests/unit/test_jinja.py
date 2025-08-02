from jinja2 import Environment, FileSystemLoader
from jinja2 import Template as JinjaTemplate

from blueprint.jinja import Jinja

bp = breakpoint


def test_jinja():
    jinja = Jinja()

    assert jinja


def test_jinja_paths():
    jinja = Jinja()
    jinja.paths = "."

    assert jinja.paths == ["."]


def test_jinja_fs(tmp_path):
    """
    GIVEN: A jinja object with ._paths set
    WHEN:  .fs is accessed
    THEN:  a FileSystemLoader should be returned
    AND:   it should have its searchpath set to ._paths
    """
    tmp_path / "tpl.jinja"
    tmp_path.touch()

    jinja = Jinja()
    jinja._paths = [tmp_path]

    assert isinstance(jinja.fs, FileSystemLoader)
    assert jinja.fs.searchpath == [str(tmp_path)]


def test_jinja_env():
    jinja = Jinja()
    jinja._fs = FileSystemLoader(["."])

    assert isinstance(jinja.env, Environment)
    assert "capitalize" in jinja.env.filters
    assert "upper" in jinja.env.filters


def test_jinja_template(tmp_path):
    """
    GIVEN: A Jinja object with .fs set
    AND:   A ._fs value set to a FileSystemLoader
    AND:   a template file in one of its search path dirs
    WHEN:  .template(filename) is called
    THEN:  it should return the template for that file
    """
    file = (tmp_path / "tpl.jinja")
    file.touch()

    jinja = Jinja()
    jinja._fs = FileSystemLoader([tmp_path])
    tpl = jinja.template("tpl.jinja")

    assert isinstance(tpl, JinjaTemplate)
    assert tpl.filename == str(file)


def test_jinja_render_string():
    jinja = Jinja()
    text = jinja.render("Hello {{ NAME | title}}.", NAME="there")

    assert text == "Hello There."


def test_jinja_render_template(tmp_path):
    file = tmp_path / "tpl.jinja"
    file.write_text("Hello {{ NAME | title}}.")

    jinja = Jinja()
    jinja._paths = [tmp_path]
    text = jinja.render(file="tpl.jinja", NAME="there")

    assert text == "Hello There."
