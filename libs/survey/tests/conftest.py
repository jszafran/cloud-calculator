import pathlib

import pytest


@pytest.fixture
def test_root_dir() -> pathlib.Path:
    return pathlib.Path(__file__).parent


@pytest.fixture
def test_data_dir(test_root_dir) -> pathlib.Path:
    return test_root_dir / "test_data"
