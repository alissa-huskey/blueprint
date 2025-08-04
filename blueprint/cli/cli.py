"""Command Line Interface."""

from bdb import BdbQuit

import click
import rich_click as click  # noqa

from blueprint import UserError
from blueprint.cli.app import App
from blueprint.cli.blueprints import blueprints
from blueprint.cli.new import new

bp = breakpoint

app = App()


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def blueprint(*args, **kwargs):
    """Project blueprints."""


blueprint.add_command(blueprints)
blueprint.add_command(new)


def run():
    """Start the command line interface."""
    try:
        blueprint()
    except UserError as e:
        app.error(e.message)
        exit(e.status)
    except BdbQuit:
        ...
    except SystemExit as ex:
        exit(ex.code)


if __name__ == "__main__":
    run()
