import json

import pytest

SCHEMA_PATH = "tests/data/nextflow_schema.json"


@pytest.fixture
def real_schema():
    """Read in a real schema for testing
    """
    with open(SCHEMA_PATH, encoding="utf8") as file_in:
        return json.load(file_in)
