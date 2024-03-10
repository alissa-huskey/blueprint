import pytest

from new_project.python_project import PythonProject


def test_python_project():
    project = PythonProject()
    assert project


def test_python_project_create(tmp_path):
    """
    WHEN: project.create is called
    THEN: A new project is created
    """
    project = PythonProject("myproject", path=tmp_path)
    project.create()

    assert (tmp_path/"myproject").is_dir()
