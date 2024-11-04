import os
import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

console = Console()


def run_command(cmd, description):
    """Run a command and print detailed output"""
    console.print(f"[bold blue]Running:[/] {description}...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        console.print(f"[bold green]Success:[/] {description}")
        return result
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error during {description}:")
        console.print(f"Command failed: {' '.join(cmd)}")
        console.print(Panel(e.stderr, title="Error Output", border_style="red"))
        raise


def create_binary_debug():
    """Creates a binary executable with support for src directory structure."""
    console.print(Panel.fit("Starting binary build process", title="Build Process"))

    # Check current directory
    current_dir = Path.cwd()
    console.print(f"\nWorking directory: [cyan]{current_dir}[/]")

    # Check src directory structure
    src_dir = current_dir / "src" / "workflow_scripts"
    if not src_dir.exists():
        raise FileNotFoundError(f"Source directory not found at {src_dir}")
    console.print(f"[green]Found source directory:[/] {src_dir}")

    # Verify pyproject.toml exists
    if not os.path.exists("pyproject.toml"):
        raise FileNotFoundError("No pyproject.toml found. Are you in the right directory?")
    console.print("[green]Found pyproject.toml[/]")

    # Verify poetry is installed
    try:
        run_command(["poetry", "--version"], "Checking Poetry installation")
    except FileNotFoundError:
        console.print("[red]Poetry not found. Please install Poetry first:[/]")
        console.print("pip install poetry")
        return

    # Install PyInstaller in the poetry environment
    run_command(["poetry", "add", "--group=dev", "pyinstaller"], "Installing PyInstaller")

    # Get the project name from pyproject.toml
    project_info = run_command(["poetry", "version"], "Getting project name")
    project_name = project_info.stdout.split()[0]
    console.print(f"Project name: [cyan]{project_name}[/]")

    # List all Python files in src directory
    py_files = list(src_dir.glob("**/*.py"))
    if not py_files:
        console.print(f"[red]No Python files found in {src_dir}![/]")
        return

    # Try to identify main file
    main_candidates = [
        f for f in py_files if f.name in ["main.py", "app.py", "__main__.py", "cli.py"]
    ]

    if not main_candidates:
        console.print("\nAvailable Python files:", style="bold")
        for idx, file in enumerate(py_files, 1):
            console.print(f"{idx}. {file.relative_to(current_dir)}")

        try:
            idx = int(console.input("\nEnter the number of your main file: ")) - 1
            main_file = py_files[idx]
        except (ValueError, IndexError):
            console.print("[red]Invalid selection[/]")
            return
    else:
        main_file = main_candidates[0]

    console.print(f"\nUsing [cyan]{main_file.relative_to(current_dir)}[/] as entry point")

    # Create spec file for src directory structure
    spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    [r'{main_file!s}'],
    pathex=[r'{current_dir!s}'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{project_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""

    spec_file = current_dir / "build.spec"
    with open(spec_file, "w") as f:
        f.write(spec_content)

    # Build the binary using PyInstaller
    console.print(Panel.fit("Building binary", title="Build Progress"))
    build_cmd = ["poetry", "run", "pyinstaller", "--clean", str(spec_file)]

    console.print(f"Executing command: [blue]{' '.join(build_cmd)}[/]")

    try:
        run_command(build_cmd, "Building with PyInstaller")
    except subprocess.CalledProcessError:
        console.print("\n[red]Build failed. Please check the error messages above.[/]")
        return

    # Verify the dist directory and binary were created
    dist_dir = Path("dist")
    if not dist_dir.exists():
        console.print("[red]Build completed but dist directory was not created![/]")
        return

    binary_name = f"{project_name}.exe" if sys.platform == "win32" else project_name
    binary_path = dist_dir / binary_name

    if binary_path.exists():
        size_mb = binary_path.stat().st_size / (1024 * 1024)
        console.print(
            Panel.fit(
                f"[green]Binary successfully created![/]\n"
                f"Location: {binary_path.absolute()}\n"
                f"Size: {size_mb:.1f} MB",
                title="Build Complete",
            )
        )
    else:
        console.print(
            f"[red]Build process completed but binary not found at expected location: {binary_path}[/]"
        )


if __name__ == "__main__":
    try:
        create_binary_debug()
    except Exception as e:
        console.print(f"\n[red]Build failed with error:[/] {e!s}")
        raise
