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


def test_project_path_valid(tmp_path):
    project = Project()
    project.path = tmp_path
    assert project.path == tmp_path


@pytest.mark.skip
def test_project_create(tmp_path):
    """
    WHEN: project.create is called
    THEN: A new project is created
    """
    project = Project("myproject", path=tmp_path)
    project.create()

    assert (tmp_path/"myproject").is_dir()
