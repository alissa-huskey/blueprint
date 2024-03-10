import pytest

from new_project import AccessError
from new_project.project import Project


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
