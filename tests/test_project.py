from contextlib import contextmanager

import pytest

from blueprint import AccessError, ProgramError
from blueprint.project import Project


@contextmanager
def modify_class_sources(klass, sources):
    """Temporarily modify the SOURCES directory of a Project class."""
    orig = klass.SOURCES
    klass.SOURCES = sources
    yield
    klass.SOURCES = orig


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


def test_project_path(tmp_path):
    project = Project("some-project")
    project.dest = tmp_path
    assert project.path == tmp_path/"some-project"


def test_project_create(tmp_path):
    """
    WHEN: project.create is called
    THEN: A new project is created
    """
    project = Project("myproject", dest=tmp_path)
    project.create()

    assert (tmp_path/"myproject").is_dir()


def test_project_snake_name():
    """
    WHEN: project.snake_name is accessed
    THEN: it should return the snake tail version of that name
    """
    project = Project("my-project")

    assert project.snake_name == "my_project"


def test_project_pascal_name():
    """
    WHEN: project.pascal_name is accessed
    THEN: it should return the pascal tail version of that name
    """
    project = Project("my-project")

    assert project.pascal_name == "MyProject"


def test_project_title_name():
    """
    WHEN: project.pascal_name is accessed
    THEN: it should return the pascal tail version of that name
    """
    project = Project("my-project")

    assert project.title_name == "My Project"


def test_project_source_file():
    """
    GIVEN: a Project object
    WHEN: project.source_file() is called with a filename in the same class
    THEN: the path to file in the SOURCES dir for that class is returned
    """
    project = Project()
    path = project.source_path("README.md")
    assert path == Project.SOURCES / "README.md"


def test_project_source_file_subclass(tmp_path):
    """
    GIVEN: a Project subclass
    AND: a file exists in the SOURCES dir for that class
    WHEN: project.source_file() is called with a filename in the same class
    THEN: the path to file in the SOURCES dir for that class is returned
    """

    source_path = tmp_path / "special_file"
    source_path.touch()

    class StubProject(Project):
        SOURCES = tmp_path

    project = StubProject()
    path = project.source_path("special_file")

    assert path == source_path


def test_project_source_file_subclass_inherit(tmp_path):
    """
    GIVEN: a Project subclass
    AND: a file does not exist in the SOURCES dir for that class
    AND: a file exists in the SOURCES dir for a parent class
    WHEN: project.source_file() is called with a filename in the same class
    THEN: the path to file in the SOURCES dir for the parent class is returned
    """

    class StubProject(Project):
        SOURCES = tmp_path

    project = StubProject()
    path = project.source_path("README.md")
    assert path == Project.SOURCES / "README.md"


def test_project_source_file_subclass_inherit_overwrite(tmp_path):
    """
    GIVEN: a Project subclass
    AND: a file exists in the SOURCES dir for that class
    AND: a file exists in the SOURCES dir for the parent class
    WHEN: project.source_file() is called with a filename in the same class
    THEN: the path to file in the SOURCES dir for that class is returned
    """
    source_path = tmp_path / "README.md"
    source_path.touch()

    class StubProject(Project):
        SOURCES = tmp_path

    project = StubProject()
    path = project.source_path("README.md")

    assert path == source_path


def test_project_source_file_subclass_inherit_none(tmp_path):
    """
    GIVEN: a Project subclass
    AND: no file exists in the SOURCES dir for that class
    AND: no file exists in the SOURCES dir for any parent class
    WHEN: project.source_file() is called with a filename in the same class
    THEN: None should be returned
    """
    class StubProject(Project):
        SOURCES = tmp_path

    project = StubProject()

    with pytest.raises(ProgramError):
        project.source_path("missing-file")


def test_project_install(tmp_path):
    """
    GIVEN: a project object where create() has been called
    WHEN: project.install() is called with a valid filename from the sources
          directory
    THEN: The file should exist in the new project
    """
    project = Project("myproject", dest=tmp_path)
    project.create()
    project.install("README.md")

    assert (project.path / "README.md").is_file()


def test_project_install_is_dir(tmp_path):
    """
    GIVEN: a project object where create() has been called
    WHEN: project.install(DIRNAME, is_dir=True) is called with a valid source directory
    THEN: a matching direcory should be created in the new project
    """
    proj_path = tmp_path / "project"
    proj_path.mkdir()
    source_path = tmp_path / "sources"
    some_dir = source_path / "some_dir"
    some_dir.mkdir(parents=True)

    with modify_class_sources(Project, source_path):
        project = Project("myproject", dest=proj_path)
        project.create()
        project.install("some_dir")

    assert some_dir.is_dir()


@pytest.mark.skip("how to test this with no sources/bare/SNAKE_CASE?")
def test_project_install_path_subs(tmp_path):
    """
    GIVEN: a Project object where create() has been called
    WHEN: project.install() is called with a valid filename from the sources
          directory
    THEN: The file should exist in the new project
    """
    project = Project("my-project", dest=tmp_path)
    project.create()
    project.install("SNAKE_NAME/__init__.py")

    assert (project.path / "my_project" / "__init__.py").is_file()


def test_project_install_file_subs(tmp_path):
    """
    GIVEN: a Project object where create() has been called
    AND: a file exists with a template variable
    WHEN: project.install() is called with that filename
    THEN: The variable name should be replaced with the right value
    """
    project = Project("my-project", dest=tmp_path)
    project.create()
    project.install("README.md")

    dest_file = project.path / "README.md"
    dest_contents = dest_file.read_text()

    assert "My Project" in dest_contents


def test_project_install_all(tmp_path):
    """
    GIVEN: a Project object where create() has been called
    WHEN: project.install_all() is called
    THEN: The files should exist in the new project
    """
    project = Project("myproject", dest=tmp_path)
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
    project = Project("myproject", dest=tmp_path)
    project.create()
    project.setup()

    assert (project.path / ".git").is_dir()
