Blueprint
=========

A personal project for creating new projects from blueprints.

Usage
-----

```text
 Usage: bp new BLUEPRINT [OPTIONS] NAME

╭─ Arguments ────────────────────────────────────────╮
│ *  NAME    TEXT  [required]                        │
╰────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────╮
│ --dest     -d  PATH  Where to create the project.  │
│ --summary  -s  TEXT  One line project description. │
│ --license  -l  TEXT  Project license.              │
│ --author   -a  TEXT  Project author's name.        │
╰────────────────────────────────────────────────────╯
```

> All blueprints use these options and arguments, though additional
> options and arguments may be available depending on the blueprint.

Available Blueprints
--------------------

Blueprints are stored in the [plans/](plans/) directory.

```text
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Name          ┃ Title            ┃ Description                       ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ python-poetry │ Python: Poetry   │ Python project managed by poetry. │
│ basic         │                  │ Generic project.                  │
│ phpbb-ext     │ phpBB Extension  │ phpBB Extension                   │
└───────────────┴──────────────────┴───────────────────────────────────┘
```

Examples
--------

Simple examples can be found in the [examples/](examples/) directory. Full
working blueprints can be viewed in the [plans/](plans/) directory.

Here is an example of a minimal blueprint.

### Directory Structure

```text
plans/prose
|-- blueprint.json
|-- skeleton/
|   |-- drafts/
|   |   `-- {{DASH_NAME}}.md
|   |-- final/
|   |   `-- .ignore
|   |-- outline/
|   |   `-- story-outline.md
|   `-- research/
|       `-- notes.md
`-- tests/
    |-- helper.bash
    `-- new.bats
```

### blueprint.json

```json
{
  "name": "prose",
  "title": "Prose",
  "description": "Writing projects.",
  "version": "0.1.0",
  "type": "generic",
  "parent": "basic"
}
```

 > The full example can be found at [examples/prose](examples/prose).

Blueprints
----------

Blueprints reside in the `plans/` directory.

Each blueprint directory requires, at minimum, a `blueprint.json` file. Most
blueprint directories will also include a `skeleton/` directory, which contains
the file and directories that will be created in the projects.

A `tests/` directory is strongly recommended, which should contain one or more
[Bats][] tests to verify that the project is created as expected.


### Directory Structure

|   | Name             | Description                                                                 |
|---|------------------|-----------------------------------------------------------------------------|
|   | `blueprint.json` | Specifications for this blueprint. (See [blueprint.json](#blueprintjson-1).) |
| T | `after/`         | Files to be added after all other steps.                                    |
| T | `skeleton/`      | Project directory structure.                                                |
|   | `tests/`         | [Bats][] tests to validate that blueprint commands function as expected.    |
| T | `templates/`     | Jinja templates specific to this blueprint.                                 |
|   | `scripts/`       | Scripts to execute during `setup`, `after`, or `variables` steps.           |

Legend: **T**: File and directory names and contents rendered via [Jinja][].

[Bats]: https://bats-core.readthedocs.io/en/stable/

### blueprint.json

The `blueprint.json` file defines the blueprint's specifications. The `"type"`
property identifies the blueprint [type](#types), which will effect the
required properties.

The values of some properties like `"setup"` and `"after"` may contain
[#Executable](#executables) values, which are runnable instructions.

For the full `blueprint.json` specification, see the [JSON schemas](schemas/).

#### Properties

All blueprints are based on the `base.schema.json` schema. Depending on the
value of the `"type"` property, other properties may be required or available.

##### List

<details><summary>Property list</summary>

|   |   | Property Name       | Type   | Description                                            | Example                                                                                                         |
|---|---|---------------------|--------|--------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| * |   | name                | string | The unique identifier for this Project Type.           | `"python-poetry"`                                                                                               |
|   |   | title               | string | Human readable title.                                  | `"Python Poetry Project"`                                                                                       |
| * |   | description         | string | Brief description                                      | `"Python project managed by Poetry"`                                                                            |
| * |   | version             | string | Version of this blueprint.                             | `"0.1.0"`                                                                                                       |
| * |   | type                | string | Blueprint type. (See [Types](#Types))                   | `"language-toolstack"`                                                                                          |
|   |   | parent              | string | Name of another blueprint to inherit from.             | `"basic"`                                                                                                       |
| + |   | stack               | object | Dev toolstack.                                         | `{"language": "python", "dependencies": "poetry", "tests": "pytest", "linter": "flake8", "formatter": "black"}` |
|   |   | project-dir         | string | Pattern for project directory name.                    | `"phpbb-{{ NAME }}"`                                                                                            |
|   |   | requirements        | string | Requirements that must be installed on system to work. | `["python", "poetry", "asdf"]`                                                                                  |
|   | E | variables           | object | Variables to define.                                   | `{ "PYTHON_EXE": { "cmd": ["asdf", "where", "python", "{PYV}"] } }`                                             |
|   |   | options             | object | CLI options.                                           | `{ "pyv": { "default": "3.10.2", "help": "Python version" } }`                                                  |
|   | E | arguments           | object | CLI argument(s).                                       | `[{ "vendor": {}, "name": {} }]`                                                                                |
|   | E | setup               | list   | List of setup steps.                                   | `[{ "cmd": ["git", "init"] }]`                                                                                  |
|   | E | after               | list   | Steps to take after all other steps.                   | `[{"install": "CodeSniffer.conf", "dest": "vendor/squizlabs/php_codesniffer/CodeSniffer.conf"}]`                |
| + |   | dependency-commands | object | Commands used to install dependencies.                 | `{ "main": ["poerty", "add"], "dev": ["poetry", "add", "--group", "dev"] }`                                     |

Legend:
**\***: Required property,
**+**: Required by some types,
**E**: [#Executable](#Executables) values

</details>

##### Types

The `"type"` property specifies a project type associated with a blueprint
schema.

| Name                  | Description                                         | Example           | Schema                                |
|-----------------------|-----------------------------------------------------|-------------------|---------------------------------------|
| Generic               | Basic project.                                      | [basic][]         | [generic.schema.json][]               |
| Framework Application | Project built on a specific framework.              | [python-typer][]  | [framework-application.schema.json][] |
| Extension             | Extension for some kind of software.                | [phpbb-ext][]     | [extension.schema.json][]             |
| Language Toolstack    | Setup for a particular language and dev toolstack.  | [python-poetry][] | [language-toolstack.schema.json][]    |

[basic]: plans/basic/blueprint.json
[python-typer]: plans/python-typer/blueprint.json
[phpbb-ext]: plans/phpbb-ext/blueprint.json
[python-poetry]: plans/python-poetry/blueprint.json

[generic.schema.json]: schemas/generic.schema.json
[framework-application.schema.json]: schemas/framework-application.schema.json
[extension.schema.json]: schemas/extension.schema.json
[language-toolstack.schema.json]: schemas/language-toolstack.schema.json

##### Executables

`#Executable` objects are runnable instructions that can be defined in
`"variables"`, `"arguments"`, `"setup"` and `"after"`.

| Name    | Action                                             |
|---------|----------------------------------------------------|
| cmd     | Execute a shell command.                           |
| install | Install a file.                                    |
| script  | Execute a script from `scripts/` directory to run. |

###### cmd

The `"cmd"` property indicates a shell command.

<details><summary>cmd object properties</summary>

|   | Name     | Type          | Description                                                     | Example                                                   |
|---|----------|---------------|-----------------------------------------------------------------|-----------------------------------------------------------|
| * | cmd      | array         | Command to execute.                                             | `["git", "init"]`                                         |
|   | options  | object        | Options to pass to script if property name evaluates to truthy. | `{ "{{ SUMMARY }}": ["--description", "{{ SUMMARY }}"] }` |
|   | env_path | string, array | Path or list of paths to prefix to PATH environment variable.   | `""/opt/homebrew/opt/php@7.4/bin""`                       |
|   | env      | object        | Environment variables.                                          |                                                           |
|   | out      | string        | Output file path.                                               | `.env`                                                    |

</details>

<details>
<summary>Examples</summary>

```json
{
    ...
    "variables": {
        "PYTHON_EXE": { "cmd": ["asdf", "where", "python", "{{ PYV }}"] }
    }
}
```

```json
{
    ...
    "setup": [
    {
        "cmd": ["echo", "{{ PYV }}"],
        "out": ".python-version"
    }
}
```

```json
{
    ...
    "after": [
        { 
            "cmd": ["composer", "install"],
            "env_path": ["/opt/homebrew/opt/php@7.4/bin"]
        }
    ]
}
```

</details>

###### install

The `"install"` property is used to install a file.

<details><summary>install object properties</summary>

|   | Name    | Type   | Description               | Example              |
|---|---------|--------|---------------------------|----------------------|
| * | install | string | Filename.                 | `"git-description"`  |
|   | dest    | string | Project destination path. | `".git/description"` |

</details>

<details><summary>Examples</summary>

```json
{
    ...
    "after" [
        {
        "install": "CodeSniffer.conf",
        "dest": "vendor/squizlabs/php_codesniffer/CodeSniffer.conf"
        }
    ]
}
```
</details>

###### script

The `"scripts"` property is used to execute a script from the `scripts/` directory.

<details><summary>script object properties</summary>

|   | Name      | Type          | Description                                                     | Example                                                   |
|---|-----------|---------------|-----------------------------------------------------------------|-----------------------------------------------------------|
| * | script    | string        | Script to execute.                                              | `"bootstrap.sh"`                                          |
|   | arguments | array         | Variables to pass to script.                                    | `["{{VERSION}}", "{{AUTHOR}}", "{{LICENSE}}"]`            |
|   | options   | object        | Options to pass to script if property name evaluates to truthy. | `{ "{{ SUMMARY }}": ["--description", "{{ SUMMARY }}"] }` |
|   | env_path  | string, array | Path or list of paths to prefix to PATH environment variable.   | `""/opt/homebrew/opt/php@7.4/bin""`                       |
|   | env       | object        | Environment variables.                                          |                                                           |
|   | out       | string        | Output file path.                                               | `.env`                                                    |

</details>

<details><summary>Examples</summary>

```json
{
    ...
    "setup": [
        ...
        {
        "script": "setup-pyproject",
        "arguments": ["{{ PATH }}", "{{ VERSION }}", "{{ PYV_CONSTRAINT }}"]
        },
        ...
    ]
}
```

</details>

### Templates

[Jinja][] is used to render file and directory names and contents inside the
`after/`, `skeleton/` and `templates/` directories.

#### Filters

Blueprint provides a few custom Jinja filters.

<details><summary>Filter list</summary>

| Filter             | Description            | Example      |
|--------------------|------------------------|--------------|
| `to_camel_case`    | Camel-case.            | `"acmeInc"`  |
| `to_kebab_case`    | Kebab-case.            | `"acme-inc"` |
| `to_pascal_case`   | Pascal-case.           | `"AcmeInc"`  |
| `to_smooshed_case` | Lower-case, no spaces" | `"acmeinc"`  |
| `to_snake_case`    | Snake-case.            | `"acme_inc"` |
| `to_title_case`    | Title-case.            | `"Acme Inc"` |

</details>

#### Variables

In addition to the variables listed below, `"options"`, `"arguments"` and
`"variables"` properties specified in the `blueprint.json` file will be
available as template variables.

<details><summary>Variable list</summary>

| Variable                | Description                          | Example                            |
|-------------------------|--------------------------------------|------------------------------------|
| `DOT`[^dot]             | Literal `"."`.                       | `"."`                                |
| `NAME`                  | Project name as entered.             | `"my project"`                       |
| `VERSION`               | Project version number.              | `"0.1.0"`                            |
| `SUMMARY`               | Single line project description.     | `"My project that does stuff."`      |
| `LICENSE`               | Project license.                     | `"MIT"`                              |
| `AUTHOR`                | Project author name.                 | `"Jane Doe \<jane.doe@fake.com\>"`   |
| `DASH_NAME`[^_name]     | Kebab-case project name.             | `"my-project"`                       |
| `PASCAL_NAME`[^_name]   | Pascal-case project name.            | `"MyProject"`                        |
| `SMOOSHED NAME`[^_name] | Lower-case project name, no spaces"  | `"myproject"`                        |
| `SNAKE_NAME`[^_name]    | Snake-case project name.             | `"my_project"`                       |
| `TITLE_NAME`[^_name]    | Title-case project name.             | `"My Project"`                       |
| `PLAN_ROOT`             | Root directory to project blueprint. | `"~/.config/blueprint/plans/basic"` |
| `PATH`                  | Project directory.                   | `"~/projects/my-project"`            |
| `DEST`                  | Project parent directory.            | `"~/projects"`                       |

</details>

[^dot]: The `DOT` variable is for use with dotfile names, to prevent them from being evaluated in the context of the blueprint project's plan directory. For example, a file might be named `"{{DOT}}gitignore` instead of `.gitignore`
[^_name]: The various `_NAME` variables are convenience variables for file or directory names. In most cases filters can be used, for example `{{ NAME | to_pascal }}`.

[Jinja]: jinja.palletsprojects.com/en/stable/

Config
------

Config files for individual blueprints are located at
`~/.config/blueprint/BLUEPRINT.yml`.

At present, these files are used to specify dependencies and dev dependencies to add to a project.

Status
------

**Pre-alpha**

Works for me. Usually. Probably.

Unsuitable for not-me users.

Alternatives
------------

* [Cookiecutter](https://www.cookiecutter.io/)
* [yeoman](https://yeoman.io/)
* Github [template repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository)

### Why use blueprint instead?

You shouldn't. The above projects are mature and reliable, while blueprint is... not.

That being said, I wrote it because I wanted to create projects with scripting
steps--like `poetry new` or `npm init`. And now I kinda like it.

Meta
----

* Github: [alissa-huskey/blueprint][github]
* License: MIT

[github]: https://github.com/alissa-huskey/blueprint
