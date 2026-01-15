from valohai_yaml.utils.markdown_doc import generate_schema_doc
from valohai_yaml.utils.markdown_doc.formatters import format_property
from valohai_yaml.utils.markdown_doc.parsers import parse_definition, parse_top_level_item_refs
from valohai_yaml.validation import get_json_schema


def test_parse_generated_schema_doc():
    """The generated markdown documentation is parsable."""
    schema = get_json_schema()
    assert generate_schema_doc(schema), "Should generate non-empty documentation"


def test_parse_top_level_refs():
    """The main items are parsed from the schema."""
    items = {
        "properties": {
            "endpoint": {
                "$ref": "/schemas/endpoint",
            },
            "pipeline": {
                "$ref": "/schemas/pipeline",
            },
        },
    }

    assert list(parse_top_level_item_refs(items)) == [
        "/schemas/endpoint",
        "/schemas/pipeline",
    ]


def test_parse_definition():
    """Parsing a simple definition."""
    step_definition = {
        "$id": "https://valohai.com/schemas/step",
        "title": "Step Definition",
        "properties": {
            "category": {
                "description": "Category name to group & organize steps in the UI",
                "type": "string",
            },
        },
        "type": "object",
    }
    parsed_definition = parse_definition(step_definition)
    assert parsed_definition.title == "step", "Should use title from $id to match actual value in YAML"
    assert parsed_definition.description == ""
    assert parsed_definition.type == "object"
    assert parsed_definition.properties.keys() == {"category"}
    assert parsed_definition.properties["category"].keys() == {"description", "type"}
    assert parsed_definition.required_properties == []


def test_parse_refs():
    """Making internal links from $ref strings."""
    properties_definition = {
        "$ref": "https://example.com/schemas/prop_name",
    }
    formatted_properties = list(format_property(properties_definition, indentation_level=1))
    assert formatted_properties == ["    - [`prop_name`](#prop_name)"], "Should create internal markdown link"
