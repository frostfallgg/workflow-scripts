"""Functions for file system operations."""

import shutil
from pathlib import Path

from workflow_scripts.functions import package_json


def create_dist_dir(dist_dir: Path, root_json: dict):
    """Create a distribution directory.

    Args:
        dist_dir: The directory to create.
        root_json: The package.json data for the build package.

    """
    dist_dir.mkdir()
    out_dir = dist_dir / "out"
    out_dir.mkdir()
    package_path = dist_dir / "package.json"
    package_json.set_package_properties(root_json)
    package_json.write_json(package_path, root_json)


def clear_dir(dir: Path):
    """Clear the contents of a directory.

    Args:
        dir: The directory to clear.

    """
    for item in dir.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        elif item.is_file():
            item.unlink()


def copy_dir(src: Path, dest: Path):
    """Copy the contents of a directory to another directory, do not include the directory itself.

    Args:
        src: The source directory.
        dest: The destination directory.

    """
    for item in src.iterdir():
        if item.is_dir():
            shutil.copytree(item, dest / item.name)
        elif item.is_file():
            shutil.copy(item, dest / item.name)
