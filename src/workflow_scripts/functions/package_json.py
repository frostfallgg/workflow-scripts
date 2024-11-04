"""Functions for manipulating package.json files."""

import json
from pathlib import Path


def load_json(file_path: Path):
    """Load file into a dictionary, if the file is not valid JSON, return an empty dictionary.

    Args:
        file_path: The path to the JSON file.

    Returns:
        The dictionary representation of the JSON file.

    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}

def write_json(file_path: Path, data: dict):
    """Write a dictionary to a JSON file.

    Args:
        file_path: The path to the JSON file.
        data: The dictionary to write.

    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def set_package_properties(data: dict):
    """Set the properties needed to make a roblox-ts package.

    The package.json for a roblox-ts package needs some extra properties
    compared to a game package.

    Args:
        data: The dictionary to add properties to.

    """
    data["main"] = "out/init.luau"
    data["types"] = "out/index.d.ts"
    data["publishConfig"] = {"access": "public"}
    data["files"] = ["out", "!**/*.tsbuildinfo"]
    del data["scripts"]


