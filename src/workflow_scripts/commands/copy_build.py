"""CLI command to copy the build output to distribution directory.

Copies compiled Luau files from root/out to dist/out. If dist has not been created
it will set up the directory structure including the package.json file.

"""

import os
from pathlib import Path

from workflow_scripts.functions import file_io, package_json
from workflow_scripts.util import console


def cmd_copy_build(dist_name: str):
    """Copy the build output to the distribution directory."""
    root_dir = Path(os.getcwd())
    root_package = root_dir / "package.json"
    source_build = root_dir / "out"

    if not source_build.exists() or not source_build.is_dir():
        console.semantic("No build output found in the root directory.", type="error")
        return

    if not root_package.exists() or not root_package.is_file():
        console.semantic("No package.json file found in the root directory.", type="error")
        return

    dist_dir = root_dir / dist_name
    out_dir = dist_dir / "out"
    if not dist_dir.exists() or not dist_dir.is_dir():
        file_io.create_dist_dir(dist_dir, package_json.load_json(root_package))
        console.semantic("Distribution directory created.", type="info")

    file_io.clear_dir(out_dir)
    file_io.copy_dir(source_build, out_dir)

    console.semantic("Build output copied to distribution directory.", type="success")
