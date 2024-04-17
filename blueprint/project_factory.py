"""Image Factory module."""

from blueprint.project import Project
from blueprint.python_project import PythonProject


class ProjectFactory:
    """Project factory."""

    def __new__(cls, name=None, dest=None, **kwargs):
        """Return Project object.

        Instantiate a project object with the correct class depending on the
        CLI arguments.
        """
        klass = Project
        is_python = kwargs.pop("python", None)

        if is_python:
            klass = PythonProject

        return klass(name, dest)
