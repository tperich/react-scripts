#!/bin/env python3
"""Creates a TypeScript component.

The script uses templates from ./templates folder to place a predefined
component file structure inside src/components folder.
"""

import sys
import shutil
import argparse
from pathlib import Path


def parse_arguments() -> dict:
    """Creates and parses argparse arguments.

    Returns:
        dict: A dictionary containing passed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Creates components out of thin air")
    parser.add_argument("-n", "--name", required=True,
                        help="Name of the component")

    return parser.parse_args()


def get_root_path() -> Path:
    """Dinamically returns script's root path.
    
    Returns:
        current: Current working directory as Path.
    """
    current = Path.cwd()
    if current.parts[-1] == "scripts":
        current = current.parent
    return current


def read_template(file_name: str) -> str:
    """Reads file template from templates folder.
    
    Args:
        file_name: Name of the template file.
    Return:
        template: Template file as a string.
    """
    current = get_root_path()
    file_path = current.joinpath(f"scripts/templates/{file_name}")
    if not Path.exists(file_path):
        print(f"Error: the template is missing for {file_path}")
        sys.exit(1)

    template = ""
    with open(file_path, "r") as f:
        template = f.read()

    return template


def create_component(name: str) -> None:
    """Creates component files.

    Args:
        name: Component name to be created.
    """
    print(f"Creating component {name}")

    current = get_root_path()
    base_dir = current.joinpath("src/components")
    component_path = base_dir.joinpath(name)

    if Path.is_dir(component_path):
        warn_msg = "WARNING: Already exists, are you sure you wish to remove this? y/N: "
        choice = input(warn_msg)

        if choice == ("y" or "Y"):
            shutil.rmtree(component_path)
        else:
            sys.exit()

    Path.mkdir(component_path)

    print("Creating index.ts...")
    with open(f"{component_path}/index.ts", "w") as f:
        f.write(read_template("index.ts").replace("component", name))

    print(f"Creating {name}.tsx...")
    with open(f"{component_path}/{name}.tsx", "w") as f:
        f.write(read_template("component.tsx").replace("component", name))

    print(f"Creating {name}.scss...")
    with open(f"{component_path}/{name}.scss", "w") as f:
        f.write(read_template("component.scss"))

    print("Done!")


if __name__ == "__main__":
    ARGS = parse_arguments()
    create_component(ARGS.name)
