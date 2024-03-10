"""Command Line Interface."""

from typer import Typer

from new_project import NewProjectError
from new_project.app import App

cli = Typer()
app = App()


@cli.command()
def hello():
    """Example command."""
    print("hello")


def run():
    """CLI Runner."""
    try:
        cli()
    except NewProjectError as e:
        app.error(e.message)
        app.exit(e.status)
    except SystemExit:
        ...
    except BaseException:
        breakpoint()
        ...


if __name__ == "__main__":
    run()
