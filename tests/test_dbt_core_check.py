from pathlib import Path
import  os

import pytest

from pre_commit_hooks.dbt_core_check import check


@pytest.mark.parametrize("file,expected", [
    ("dbt/adapters/factory.py", 0),
    ("dbt/adapters/postgres/impl.py", 1),
    ("dbt/tests/adapter", 0),
]
)
def test_module(file: str, expected: int):
    project_root = Path(__file__).parents[1]
    path = project_root / file
    assert path.exists()
    assert check(path) == expected
