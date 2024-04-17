"""Command Line Interface."""

from blueprint import BlueprintError
from blueprint.app import App
from typer import Typer

cli = Typer()
app = App()


@cli.command()
def hello():
    """Demonstrate example command."""
    print("hello")


def run():
    """CLI Runner."""
    try:
        cli()
    except BlueprintError as e:
        app.error(e.message)
        app.exit(e.status)
    except SystemExit:
        ...
    except BaseException:
        breakpoint()
        ...


if __name__ == "__main__":
    run()
