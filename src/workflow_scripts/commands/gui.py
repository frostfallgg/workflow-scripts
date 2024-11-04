"""GUI command which allows access to all the tools."""

import os
import sys

from rich.console import Console
from rich.panel import Panel

from workflow_scripts.commands.copy_build import cmd_copy_build
from workflow_scripts.commands.update_build import cmd_update_build

console = Console()

current_selection: int = 1
cmds = [
    ["Copy output to distribution", cmd_copy_build],
    ["Update distribution package.json", cmd_update_build],
    ["Exit", lambda dist: sys.exit()],
]


def present_commands(message="Select a command"):
    """Present the available commands."""
    selection = 0
    os.system("cls")
    console.print(Panel.fit(message, title="Tools"))
    for i, cmd in enumerate(cmds, 1):
        console.print(f"[white]{i}. {cmd[0]}[/]")

    usr_input = input()
    try:
        selection = int(usr_input)
        if selection > 0 and selection <= len(cmds):
            return selection
        return present_commands(
            f"[red]Invalid selection. Please enter a number in range 1-{len(cmds)}.[/]"
        )

    except ValueError:
        return present_commands(
            f"[red]Invalid selection. Please enter a number in range 1-{len(cmds)}.[/]"
        )


def cmd_gui():
    """Run the GUI."""
    running = True
    while running:
        chosen = present_commands()
        if chosen:
            cmds[chosen - 1][1]("dist")
            running = False
