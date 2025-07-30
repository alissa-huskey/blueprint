import pytest

from blueprint import AccessError
from blueprint.object import Object
from blueprint.project import Project
from blueprint.template import Template
from tests.unit import set_config_base, set_templates_root

bp = breakpoint


def test_project():
    project = Project()
    assert project


def test_project_path_invalid():
    with pytest.raises(AccessError):
        project = Project()
        project.dest = "invalid_directory"


def test_project_dest_valid(tmp_path):
    project = Project()
    project.dest = tmp_path
    assert project.dest == tmp_path


def test_project_template():
    project = Project("basic")

    assert project.template == Template("basic")


def test_project_path(tmp_path):
    project = Project(name="some-project")
    project.dest = tmp_path
    assert project.path == tmp_path/"some-project"


def test_project_substitute():
    project = Project(name="my-project")
    text = project.substitute("${SMOOSHED_NAME}")

    assert text == "myproject"


def test_project_create(tmp_path):
    """
    WHEN: project.create is called
    THEN: A new project is created
    """
    project = Project("basic", "myproject", dest=tmp_path)
    project.create()

    assert (tmp_path/"myproject").is_dir()


def test_project_create_parent(tmp_path):
    """
    WHEN: project.create is called
    THEN: A new project is created
    """
    project = Project("python-poetry", "myproject", dest=tmp_path)
    project.create()

    assert (tmp_path/"myproject").is_dir()


def test_project_dash_name():
    """
    WHEN: project.dash_name is accessed
    THEN: it should return the dash version of that name
    """
    project = Project(name="my_project")

    assert project.dash_name == "my-project"


def test_project_smooshed_name():
    """
    WHEN: project.snake_name is accessed
    THEN: it should return the snake tail version of that name
    """
    project = Project(name="my-project")

    assert project.smooshed_name == "myproject"


def test_project_snake_name():
    """
    WHEN: project.snake_name is accessed
    THEN: it should return the snake tail version of that name
    """
    project = Project(name="my-project")

    assert project.snake_name == "my_project"


def test_project_pascal_name():
    """
    WHEN: project.pascal_name is accessed
    THEN: it should return the pascal tail version of that name
    """
    project = Project(name="my-project")

    assert project.pascal_name == "MyProject"


def test_project_title_name():
    """
    WHEN: project.pascal_name is accessed
    THEN: it should return the pascal tail version of that name
    """
    project = Project(name="my-project")

    assert project.title_name == "My Project"


def test_project_install(tmp_path):
    """
    GIVEN: a project object where create() has been called
    WHEN: project.install() is called with a valid filename from the sources
          directory
    THEN: The file should exist in the new project
    """
    project = Project("basic", "myproject", dest=tmp_path)
    project.create()
    project.install("README.md")

    assert (project.path / "README.md").is_file()


def test_project_install_subdir(tmp_path):
    """
    GIVEN: a project object where create() has been called
    WHEN: project.install() is called with a path that is in a subdirectory
    THEN: The file should exist in the subdirectory of the new project
    """
    project = Project("python-poetry", "my project", dest=tmp_path)
    project.create()

    project.install("tests/test_${SNAKE_NAME}.py")

    assert (project.path / "tests" / "test_my_project.py").is_file()


def test_project_install_is_dir(tmp_path):
    """
    GIVEN: a project object where create() has been called
    WHEN: project.install(DIRNAME, is_dir=True) is called with a valid source directory
    THEN: a matching direcory should be created in the new project
    """
    proj_path = tmp_path / "project"
    proj_path.mkdir()

    templates_root = tmp_path / "templates"
    some_dir = templates_root / "a_template" / "skeleton" / "some_dir"
    some_dir.mkdir(parents=True)

    with set_templates_root(templates_root):
        project = Project("a_template", "myproject", dest=proj_path)
        project.create()
        project.install("some_dir")

    assert some_dir.is_dir()


def test_project_install_path_substitues(tmp_path):
    """
    GIVEN: a Project object where create() has been called
    AND: a file or directory exists with a template variable
    WHEN: project.install() is called with that filename
    THEN: The variable name should be replaced with the right value
    """
    proj_path = tmp_path / "project"
    proj_path.mkdir()

    templates_root = tmp_path / "sources"
    some_dir = templates_root / "a_template" / "skeleton" / "${SNAKE_NAME}"
    some_dir.mkdir(parents=True)

    with set_templates_root(templates_root):
        project = Project("a_template", "my-project", dest=tmp_path)
        project.create()
        project.install("${SNAKE_NAME}")

    assert (project.path / "my_project").is_dir()


def test_project_install_file_subs(tmp_path):
    """
    GIVEN: a Project object where create() has been called
    AND: a file exists in the skeleton directory that contains variables
    WHEN: project.install() is called with that filename
    THEN: The file should exist in the project
    AND: The variables in the file should have been replaced
    """
    project = Project("basic", "my-project", dest=tmp_path)
    project.create()
    project.install("README.md")

    dest_file = project.path / "README.md"
    dest_contents = dest_file.read_text()

    assert "My Project" in dest_contents


def test_project_install_all_parent(tmp_path):
    """
    GIVEN: a Project object where create() has been called
    WHEN: project.install_all() is called
    THEN: The files should exist in the new project
    """
    project = Project("python-poetry", "myproject", dest=tmp_path)
    project.create()
    project.install_all()

    assert (project.path / "README.md").is_file()


def test_project_install_all(tmp_path):
    """
    GIVEN: a Project object where create() has been called
    WHEN: project.install_all() is called
    THEN: The files should exist in the new project
    """
    project = Project("basic", "myproject", dest=tmp_path)
    project.create()
    project.install_all()

    assert (project.path / "README.md").is_file()
    assert (project.path / ".todo").is_dir()


def test_project_setup(tmp_path):
    """
    GIVEN: a project object where create() has been called
    WHEN: project.setup() is called
    THEN: the project should be git init'd
    """
    project = Project("basic", "myproject", dest=tmp_path)
    project.create()
    project.setup()

    assert (project.path / ".git").is_dir()


def test_project_setup(tmp_path):
    """
    GIVEN: a project object where create() has been called
    WHEN: project.setup() is called
    THEN: the project should be git init'd
    """
    project = Project("basic", "myproject", dest=tmp_path)
    project.create()
    project.setup()

    assert (project.path / ".git").is_dir()


def test_project_setup_parent(tmp_path):
    """
    GIVEN: a project object where create() has been called
    WHEN: project.setup() is called
    THEN: the project should be git init'd
    """
    project = Project("python-poetry", "myproject", dest=tmp_path)
    project.create()
    project.setup()

    assert (project.path / ".git").is_dir()


def test_project_substitutions(fixtures_path):
    """
    GIVEN: A Project object
    AND: A json file that includes variables and options
    WHEN: .substitutuions is accessed
    THEN: it should include keys for the default template variables (ie DASH_NAME)
    AND: it should include keys the template options (ie PYV)
    AND: it should include keys for the template variables (ie PYTHON_EXE)
    """

    with set_templates_root(fixtures_path):
        project = Project("toolstack", "my project", pyv="3.10.2")

        subs = project.substitutions

        assert "DASH_NAME" in subs and subs["DASH_NAME"] == "my-project"
        assert "PYV" in subs and subs["PYV"] == "3.10.2"
        assert "PYTHON_EXE" in subs


class RunParams(Object):
    """."""

    def __init__(self, **kwargs):
        """."""
        kwargs.setdefault("then", "it should work")

        kwargs.setdefault("args", ["ls"])
        kwargs.setdefault("kw", {})
        kwargs.setdefault("ex_args", kwargs.get("args"))
        kwargs.setdefault("ex_kw", dict(capture_output=True, text=True))
        super().__init__(**kwargs)


@pytest.mark.parametrize("params", [
    RunParams(
        when="options=OPTIONS",
        then="present options should be added to command",
        kw=dict(options={
            "${DASH_NAME}": ["--name", "${DASH_NAME}"],
            "${SUMMARY}": ["--summary", "${SUMMARY}"],
        }),
        ex_args=["ls", "--name", "my-project"]
    ),
    RunParams(
        when="shell=true",
        then="args should be a string",
        kw=dict(shell=True),
        ex_args="ls",
        ex_kw=dict(capture_output=True, text=True, shell=True),
    ),
    RunParams(
        when="stdout=True",
        then="capture_output should be false",
        kw=dict(stdout=True),
        ex_kw=dict(capture_output=False, text=True, stdout=True),
    ),
    RunParams(
        when="cwd=CWD",
        then="cwd should be set",
        kw=dict(cwd="abc"),
        ex_kw=dict(capture_output=True, text=True, cwd="abc"),
    ),
    RunParams(when="basic args", then="should work", args=["abc"], ex_args=["abc"]),
    RunParams(
        when="substitute=True",
        then="substitutions should be replaced in command",
        args=["${DASH_NAME}"],
        kw=dict(substitute=True),
        ex_args=["my-project"],
    ),
])
def test_project_run(subprocess_run_mock, params):
    mock = subprocess_run_mock
    project = Project(name="my project")
    project.run(params.args, **params.kw)

    call = mock.call_args_list[0]

    message = (
        f"When .run() is called with {params.when} then {params.then} "
        f"({mock.call_args()})"
    )

    assert call.args == (params.ex_args,), message
    assert call.kwargs == params.ex_kw, message


def test_project_add_dependencies(subprocess_run_mock, tmp_path, config_yml):
    mock = subprocess_run_mock
    file = tmp_path / "python-poetry.yml"
    file.write_text(config_yml)

    with set_config_base(tmp_path):
        project = Project(name="my project", template="python-poetry")
        project.add_dependencies()

        calls = mock.call_args_list
        dependencies = [call.args[0][-1] for call in calls]

        assert calls[0].args[0] == ["poetry", "add", "--group", "dev", "pytest"]
        assert dependencies == ["pytest", "pynvim", "pylama", "black"]


def test_project_script_x():
    ...
