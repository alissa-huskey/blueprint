import pytest

from blueprint.project import Project
from blueprint.project_factory import ProjectFactory
from blueprint.python_project import PythonProject


@pytest.mark.parametrize("kwargs, klass, given", [
    ({}, Project, "no project type params are passed"),
    ({"python": True}, PythonProject, "the python kwarg is truthy"),
])
def test_project_factory_project(kwargs, klass, given):
    """
    GIVEN: No other project type params.
    WHEN: a ProjectFactory object is created
    THEN: it is the correct class
    """
    project = ProjectFactory(**kwargs)

    assert project
    assert isinstance(project, klass), \
        (
            f"GIVEN {given}; "
            f"WHEN a ProjectFactory() object is created; "
            f"THEN a {klass} object should be created"
        )
