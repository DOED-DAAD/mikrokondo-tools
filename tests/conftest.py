import json

import pytest

SCHEMA_PATH = "tests/data/nextflow_schema.json"
INPUT_SCHEMA_PATH = "tests/data/schema_input.json"


@pytest.fixture
def real_schema():
    """Read in a real schema for testing nextflow_schema.json
    """
    with open(SCHEMA_PATH, 'r', encoding="utf8") as file_in:
        return json.load(file_in)

@pytest.fixture()
def real_input_schema():
    with open(INPUT_SCHEMA_PATH, 'r', encoding='utf8') as file_in:
        return json.load(file_in)