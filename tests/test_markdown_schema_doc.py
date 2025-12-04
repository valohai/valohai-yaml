from valohai_yaml.utils.markdown_doc import generate_doc, parse_definition, parse_items
from valohai_yaml.validation import get_json_schema


def test_parse_generated_schema_doc():
    """The generated markdown documentation is parsable."""
    schema = get_json_schema()
    assert generate_doc(schema), "Should generate non-empty documentation"


def test_parse_main_items():
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

    assert list(parse_items(items)) == [
        ("endpoint", "/schemas/endpoint"),
        ("pipeline", "/schemas/pipeline"),
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
    assert parsed_definition.title == "Step Definition"
    assert parsed_definition.ref == "/schemas/step"
    assert parsed_definition.description == ""
    assert parsed_definition.type == "object"
    assert parsed_definition.properties.keys() == {"category"}
    assert parsed_definition.properties["category"].keys() == {"description", "type"}
    assert parsed_definition.required_properties == []


def test_parse_definition_title_from_id():
    """The title is derived from the $id if not explicitly provided."""
    definition = {
        "$id": "https://valohai.com/schemas/custom-step",
    }
    parsed_definition = parse_definition(definition)
    assert parsed_definition.title == "Custom-Step"
