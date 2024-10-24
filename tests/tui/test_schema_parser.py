import pytest

import mikrokondo_tools.tui.schema_parser as sp



@pytest.fixture
def schema(real_schema):
    return sp.SchemaParser(real_schema)


def test_SchemaParser(schema):
    schema.parse_schema()

def test_SchemaDefinition(schema):
    definitions_k = "definitions"
    definitions = schema.schema[definitions_k]
    for k, v in definitions.items():
        scd = sp.SchemaDefinition(k, v)
        scd.parse_definition(v)
