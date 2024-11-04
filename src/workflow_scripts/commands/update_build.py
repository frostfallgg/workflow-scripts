"""CLI command to sync package.json file properties to build.

Useful for keeping dependencies and other properties
in sync between dev and build package.json files.

"""

import os
from pathlib import Path

from workflow_scripts.functions.package_json import load_json, set_package_properties, write_json
from workflow_scripts.util import console


def cmd_update_build(dist_name: str):
    """Sync the package.json files.

    Args:
        dist_name: The name of the distribution directory.

    """
    root_dir = Path(os.getcwd())
    root_package = root_dir / "package.json"
    dist_dir = root_dir / dist_name
    build_package = dist_dir / "package.json"

    if not root_package.exists() or not root_package.is_file():
        console.semantic("No package.json file found in the root directory.", type="error")
        return

    if not dist_dir.exists() or not dist_dir.is_dir():
        console.semantic("No distribution directory found.", type="error")
        return

    if not build_package.exists() or not build_package.is_file():
        console.semantic("No package.json file found in the distribution directory.", type="error")
        return

    root_json = load_json(root_package)
    set_package_properties(root_json)
    write_json(build_package, root_json)

    console.semantic("Distribution package.json updated.", type="success")
