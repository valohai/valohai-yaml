from pathlib import Path
from typing import Any, Iterator, NamedTuple
from urllib.parse import urlparse

# TODO move to types


class MainItem(NamedTuple):
    """Top-level YAML configuration item."""

    name: str
    ref: str


class Definition(NamedTuple):
    """YAML configuration definition item."""

    title: str
    ref: str
    description: str
    type: str
    properties: dict[str, dict[str, Any]]
    required_properties: list[str]


class RefComponents(NamedTuple):
    """Components extracted from a $ref string."""

    local_ref: str
    ref_title: str


def generate_doc(schema_dict: dict[str, Any]) -> str:
    """
    Generate documentation in Markdown format.

    Based on the configuration JSON schema.
    """
    main_items = parse_items(schema_dict.get("items", {}))
    definitions = parse_definitions(schema_dict.get("$defs", {}))

    return "\n".join(format_doc_content(main_items, definitions))


# TODO move to parsers module


def parse_items(items: dict[str, Any]) -> Iterator[MainItem]:
    """Parse schema items and generate Markdown documentation."""
    for main_property, prop_values in items.get("properties", {}).items():
        yield MainItem(name=main_property, ref=prop_values["$ref"])


def parse_definitions(definitions: dict[str, dict[str, Any]]) -> Iterator[Definition]:
    """Parse all definitions from the schema."""
    for definition in definitions.values():
        yield parse_definition(definition)


def parse_definition(definition: dict[str, Any]) -> Definition:
    """Parse a single definition from the schema."""
    ref = _parse_ref(definition["$id"])
    return Definition(
        title=ref.ref_title,
        ref=ref.local_ref,
        description=definition.get("description", ""),
        type=definition.get("type", "–"),  # TODO: log a warning about missing type
        properties=definition.get("properties", {}),
        required_properties=definition.get("required", []),
    )


def _parse_ref(ref_uri: str) -> RefComponents:
    """Extract the definition ID from a $ref string."""
    ref_path = urlparse(ref_uri).path
    ref_title = Path(ref_path).name.title()

    return RefComponents(ref_path, ref_title)


# TODO move to formatters module


def format_doc_content(main_items: Iterator[MainItem], definitions: Iterator[Definition]) -> Iterator[str]:
    """Format the documentation content to Markdown."""
    yield "# Valohai YAML Configuration Documentation\n"
    yield "## Top-level Properties\n"

    for line in main_items:
        yield format_item(line)

    yield "\n## Property Details"

    for d in definitions:
        yield f"\n### {d.title}\n"
        if d.description:
            yield d.description + "\n"
        yield f"- **type:** *{d.type}*"
        if d.properties:
            yield "- **properties:**"
            yield from format_property(d.properties)
        if d.required_properties:
            yield f"- **required properties:** {', '.join(sorted(f'`{prop}`' for prop in d.required_properties))}"


def format_property(prop: dict[str, Any], indentation_level: int = 1) -> Iterator[str]:
    """Format a single property to Markdown."""
    indent = "    " * indentation_level
    for prop_name, prop_values in prop.items():
        if isinstance(prop_values, dict):
            formatted_name = _format_prop_name(prop_name)
            yield f"{indent}- {formatted_name}:"
            yield from format_property(prop_values, indentation_level + 1)
        else:
            yield f"{indent}- {_format_atomic_property(prop_name, prop_values)}"


def _format_prop_name(name: str) -> str:
    """
    Format a property name to Markdown, with some special rules.

    - custom properties in the actual YAML are monospaced
    - properties part of the schema itself are not
    """
    if name in ["properties"]:
        return name
    return f"`{name}`"


def _format_atomic_property(name: str, values: Any) -> str:
    """
    Format a single atomic property to Markdown, with some special rules.

    - values entered by the user in the actual YAML are monospaced
    - required properties are formatted as a list of monospaced values.
    - enum values (e.g. type) are italicized.
    TODO: make this look nice
    """
    if name in ["additionalProperties", "type"]:
        return f"{name}: *{values}*"
    if name in ["const"]:
        return f"{name}: `{values}`"
    if name == "enum":
        return f"allowed values: {' | '.join(sorted(f'`{v}`' for v in values))}"
    if name == "required":
        return f"required properties: {', '.join(sorted(f'`{v}`' for v in values))}"
    return f"{name}: {values}"


def format_item(item: MainItem) -> str:
    """
    Format a single top item to Markdown.

    TODO: handle internal links properly.
    """
    return f"- [`{item.name}`](#{item.name})"
