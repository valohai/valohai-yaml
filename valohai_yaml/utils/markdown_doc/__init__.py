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
    ref_title = Path(ref_path).name

    return RefComponents(ref_path, ref_title)


# TODO move to formatters module


def format_doc_content(main_items: Iterator[MainItem], definitions: Iterator[Definition]) -> Iterator[str]:
    """Format the documentation content to Markdown."""
    yield "# Valohai YAML Configuration Documentation\n"
    yield "## Top-level Properties\n"

    for line in main_items:
        yield f"- [`{line.name}`](#{line.name})"

    yield "\n## Property Details"

    for d in definitions:
        yield f"\n### `{d.title}`\n"
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
    indent = _get_indentation(indentation_level)
    for prop_name, prop_values in prop.items():
        if isinstance(prop_values, dict):
            formatted_name = _format_prop_name(prop_name)
            yield f"{indent}- {formatted_name}:"
            yield from format_property(prop_values, indentation_level + 1)
        elif isinstance(prop_values, list):
            yield from _format_list_property(prop_name, prop_values, indentation_level)
        else:
            yield f"{indent}- {_format_atomic_property(prop_name, prop_values)}"


def _get_indentation(indentation_level: int) -> str:
    return "    " * indentation_level


def _format_prop_name(name: str) -> str:
    """
    Format a property name to Markdown, with some special rules.

    - custom properties in the actual YAML are monospaced
    - properties part of the schema itself are not
    """
    if name in ["properties"]:
        return name
    return f"`{name}`"


def _format_list_property(name: str, values: list[Any], indentation_level: int = 1) -> Iterator[str]:
    """
    Format a list property to Markdown, with some special rules.

    - lists of values are formatted as a list of monospaced values.
    - values entered by the user in the actual YAML are monospaced
    - list values may be objects themselves -- continue recursively
    - TODO: object values now have a clumsy "(option)" marker - improve this
    """
    indent = _get_indentation(indentation_level)
    if name == "enum":
        yield f"{indent}- allowed values: {' | '.join(sorted(f'`{v}`' for v in values))}"
    elif name == "required":
        yield f"{indent}- required properties: {', '.join(sorted(f'`{v}`' for v in values))}"
    else:
        yield f"{indent}- {name}"
        sub_indent = _get_indentation(indentation_level + 1)
        for val in values:
            if isinstance(val, dict):
                # we have a list of objects here -- continue recursively with its values
                yield f"{sub_indent}- (option)"
                yield from format_property(val, indentation_level + 2)
            else:
                yield f"{sub_indent}- {val}"


def _format_atomic_property(name: str, values: Any) -> str:
    """
    Format a single atomic property to Markdown, with some special rules.

    - values entered by the user in the actual YAML are monospaced
    - enum-type values are italicized
    """
    if name in ["additionalProperties", "type"]:
        return f"{name}: *{values}*"
    if name in ["const"]:
        return f"{name}: `{values}`"
    if name == "$ref":
        ref_name = Path(values).name
        return f"[{ref_name}](#{ref_name})"
    return f"{name}: {values}"
