import pytest

from mikrokondo_tools.format import format
from tests import conftest


@pytest.mark.parametrize(
    ("test_val", "output"),
    [
        ({"seqkit": {"type": "string"}},
            {"seqkit": {"type": "string"}}),

        ({"seqkit.singularity":
            {"type": "string"}},

            { "seqkit": {
                "type": "object",
                "properties": {
                    "singularity":
                        {"type": "string"}
                    }
                }
            }),

        ({"seqkit.singularity":
            {"type": "string"},
        "skt.singularity":
            {"type": "string"}},

        {
            "seqkit":
            {
            "type": "object",
            "properties": {
                "singularity":
                    {"type": "string"}}
            },
            "skt": {
                "type": "object",
                "properties": {"singularity":
                    {"type": "string"}}}}),

        (
            {"seqkit.singularity":
                {"type": "string"},
            "seqkit.docker":
                {"type": "string"}},

            {"seqkit":
            {  "type": "object",
                "properties":
                {"singularity":
                    {"type": "string"},
                "docker":
                    {"type": "string"}}}}
        ),
        (
            {
                "seqkit.singularity": {"type": "string"},
                "seqkit.docker": {"type": "string"},
                "seqkit.args.illumina": {"type": "string"},
                "seqkit.args.single_end": {"type": "string"},
            },
            {
            "seqkit": 
                {
                "type": "object",
                "properties": 
                    {
                    "singularity":
                        {"type": "string"},
                    "docker":
                        {"type": "string"},
                    "args": 
                        {
                            "type": "object",
                            "properties": 
                            {
                                "illumina": {"type": "string"},
                                "single_end": {"type": "string"},
                            }
                        }
                    }
                }
            }
        ),
    ],
)
def test_nest_schema(test_val, output):
    assert format.nest_schema(test_val) == output


def test_read_json(real_schema):
    assert real_schema == format.read_json(conftest.SCHEMA_PATH)

@pytest.mark.parametrize("input_,output", 
                        [("singularity", "#/definitions/singularity")
                        ])
def test_create_all_of_ref(input_, output):
    assert format.create_all_of_ref(input_) == output