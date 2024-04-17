Blueprint
=========

A personal project for creating new projects from blueprints, mostly for Python
projects.

Usage
-----

```bash
bp new TYPE [OPTIONS] NAME

Create a new project.

TYPES
    basic                 A basic project.
    python                A Python project.

ARGUMENTS
    name                  Project name.

OPTIONS
    --dest            -d  Where to create the project.
    --summary         -s  One-line project description.
    --license         -l  License of the package.
```

### Basic

The basic project is the one that all other types inherit from.

Toolchain

* git
* [todo.txt-cli](https://github.com/todotxt/todo.txt-cli)

Behavior

* Generate a `README.md` .
* Initialize git.
* Create `.todo` dir.

### Python

A Python project inherits all of the behavior and options from a basic project.

Toolchain

* poetry
* asdf

Behavior

* Create new poetry project via `poetry new` and `poetry init`.
* Modify `pyproject.toml` to add configs for `tool.pytest.ini_options` and `tool.black`.
* Install a `setup.cfg` with `flake8` options.
* Install my personal `object.py` and `attrs.py` files.
* Generate a `.python-version` file.
* Add and install a pre-defined list of dev dependencies.


```bash
bp new python [OPTIONS] NAME

Create a new Python project.

OPTIONS
    --pyv             -P  Python version to use.
    --pyv-constraint  -C  Supported Python versions.
```

Status
------

**Pre-alpha**

Works for me. Usually. Probably.

Unsuitable for not-me users.

Alternatives
------------

* [Cookiecutter](https://www.cookiecutter.io/)
* [yo](https://github.com/yeoman/yo) / [yeoman](https://yeoman.io/)
* Github [template repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository)
