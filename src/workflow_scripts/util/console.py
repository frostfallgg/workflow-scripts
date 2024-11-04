"""Utiliy functions for semantic console output using preset Rich styles."""

from typing import Literal, Optional

from rich.console import Console

console = Console()

print_dict = {
    "info": {"style": "BLUE", "tag": "INFO"},
    "warning": {"style": "YELLOW", "tag": "WARNING"},
    "error": {"style": "RED", "tag": "ERROR"},
    "success": {"style": "GREEN", "tag": "SUCCESS"},
    None: {"style": "WHITE", "tag": "LOG"},
}


def semantic(msg: str, type: Optional[Literal["info", "warning", "error", "success", None]] = None):
    """Log a message to the console with a preset style.

    Args:
        msg: The message to log.
        type: The type of message to log.

    """
    color = print_dict[type]["style"]
    tag = print_dict[type]["tag"]

    console.print(f"[{tag}]: {msg}", style=color)


def log(msg: str, style: str):
    """Log a message.

    Args:
        msg: The message to log.
        style: Rich formatting style.

    """
    console.print(msg, style=style)
