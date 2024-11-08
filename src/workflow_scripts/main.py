"""CLI entry file."""

import click
from rich.console import Console

from workflow_scripts.commands.copy_build import cmd_copy_build
from workflow_scripts.commands.gui import cmd_gui
from workflow_scripts.commands.update_build import cmd_update_build

console = Console()


@click.group()
def cli():
    """CLI entry point."""
    pass


@click.command("copy_dist")
@click.option(
    "--dist-name",
    "-d",
    default="dist",
    help="The name of the distribution directory.",
)
def copy_dist(dist_name):
    """Copy compiled luau to dist."""
    cmd_copy_build(dist_name)


@click.command("update_dist_package")
@click.option(
    "--dist-name",
    "-d",
    default="dist",
    help="The name of the distribution directory.",
)
def update_dist_package(dist_name):
    """Update the build package json file."""
    cmd_update_build(dist_name)


@click.command("gui")
def gui():
    """Run the GUI."""
    cmd_gui()


cli.add_command(copy_dist)
cli.add_command(update_dist_package)
cli.add_command(gui)

if __name__ == "__main__":
    cli()
