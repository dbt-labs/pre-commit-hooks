import argparse
import ast
from pathlib import Path
from typing import Iterator, List


Import = List[str]


def get_imports(module: Path) -> Iterator[Import]:
    with open(module) as fh:
        parsed_module = ast.parse(fh.read(), module)

    for node in ast.iter_child_nodes(parsed_module):
        if isinstance(node, ast.Import):
            imported_module = []
        elif isinstance(node, ast.ImportFrom):
            imported_module = node.module.split(".")
        else:
            continue

        for imported_object_path in node.names:
            imported_object = imported_object_path.name.split(".")
            yield imported_module + imported_object


def is_invalid_import(module: Import) -> bool:
    print(f"[Import] Evaluating {module}")
    return len(module) > 1 and module[0] == "dbt" and module[1] not in ["adapters", "include"]


def check_module(module: Path) -> int:
    print(f"[Module] Searching {module}")
    for imported_module in get_imports(module):
        if is_invalid_import(imported_module):
            imported_module_path = ".".join(imported_module)
            print(
                f"A dbt-core module is imported in {module}:"
                f" {imported_module_path}"
            )
            return 1
    return 0


def check_package(package: Path) -> int:
    print(f"[Package] Searching {package}")
    for module in package.rglob("*.py"):
        if check_module(module) == 1:
            return 1
    return 0


def check(path: Path) -> int:
    if path.is_dir():
        return check_package(path)
    elif path.is_file():
        return check_module(path)
    print(f"Unexpected path found: {path}")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", type=str, nargs="*", default="dbt")
    args = parser.parse_args()
    for filename in args.filenames:
        if check(Path(filename)) == 1:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
