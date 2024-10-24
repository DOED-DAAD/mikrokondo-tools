"""
Schema parser for json schemas

Matthew Wells: 2024-10-24
"""
from dataclasses import dataclass, fields
from functools import partial
import typing as t


import mikrokondo_tools.utils as u
logger = u.get_logger(__name__)

SCHEMA_INPUT_JSON = "https://raw.githubusercontent.com/phac-nml/mikrokondo/refs/heads/main/nextflow_schema.json"

@dataclass()
class Schema:
    title: t.Optional[str]
    description: t.Optional[str]
    default: t.Optional[str]
    type: t.Optional[str]
    enum: t.Optional[t.List[str]]
    hidden: t.Optional[bool]
    pattern: t.Optional[str]
    format: t.Optional[str]
    exist: t.Optional[bool]
    minimum: t.Optional[str]
    maximum: t.Optional[str]
    default: t.Optional[str]
    scheme: t.Optional['Schema']

class SchemaDefinition:
    """
    A class responsible for the parsing of the json schema to render a tui
    """
    __properties = "properties"
    __obj_keys = [ field.name for field in fields(Schema)]
    def __init__(self, title: str, definition: t.Dict[str, t.Dict]):
        self.title = title
        self.definition_data: t.Dict = definition

    def parse_definition(self, definition):
        """
        Parse a schema definition into its required components for rendering
        """
        p_schema = partial(Schema, **{k: self._get_definition_value(definition, k) for k in self.__obj_keys})
        for v in definition[self.__properties].values():
            print(Schema(**{k: self._get_definition_value(v, k) for k in self.__obj_keys}))
            print()

    def _get_definition_value(self, definition: t.Dict, key: str) -> t.Optional[str]:
        return definition.get(key)


class SchemaParser:
    """
    Parse the nextflow input schema for usage in creating a tui
    """

    __title_string = "title"
    __definitions = "definitions"

    def __init__(self, schema: t.Optional[t.Dict] = None):
        self.schema = schema
        if self.schema is None:
            self.schema = u.download_json(SCHEMA_INPUT_JSON, logger)

    def parse_schema(self, schema: t.Optional[t.Dict] = None):
        """
        Parse the needed field values from the json schema
        """
        if schema is None:
            schema = self.schema
        schema_title = schema[self.__title_string]
        scheme = partial(Schema, title=schema_title)
        self.create_schema_definitions(schema[self.__definitions])
        #fin_scheme = scheme()
        #print(fin_scheme)

    def create_schema_definitions(self, schema_definitions: t.Dict[str, t.Dict]):
        """
        Create a list of SchemaDeinitions for later rendering
        """
        for k, v in schema_definitions.items():
            SchemaDefinition(k, v)
