from pathlib import Path
from pkgutil import extend_path

import pytest

from pre_commit_hooks.dbt_core_in_adapters_check import check


@pytest.fixture(scope="module")
def dbt_core():
    original_path = __path__
    __path__ = extend_path(__path__, __name__)
    yield
    __path__ = original_path


@pytest.mark.parametrize("project_path,expected", [
    ("dbt/adapters/factory.py", 0),
    ("dbt/adapters/postgres/impl.py", 1),
    ("dbt/tests/adapter", 0),
    ("dbt/tests/postgres/test_one.py", 0),
    ("dbt/tests/postgres/test_two.py", 1),
    ("dbt/tests/postgres", 1),
]
)
def test_check(project_path: str, expected: int):
    absolute_path = Path(__file__).parent / project_path
    assert absolute_path.exists()
    assert check(absolute_path) == expected
