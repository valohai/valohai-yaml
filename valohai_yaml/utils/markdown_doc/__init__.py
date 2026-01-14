from pathlib import Path
from typing import Any, Iterable, Iterator, NamedTuple

# TODO move to types


class Definition(NamedTuple):
    """YAML configuration definition item."""

    title: str
    description: str
    type: str
    properties: dict[str, dict[str, Any]]
    required_properties: list[str]


def generate_doc(schema_dict: dict[str, Any]) -> str:
    """
    Generate documentation in Markdown format.

    Based on the configuration JSON schema.
    """
    top_level_item_refs = list(parse_top_level_item_refs(schema_dict.get("items", {})))
    definitions = parse_definitions(schema_dict.get("$defs", {}), top_level_item_refs)

    return "\n".join(format_doc_content(top_level_item_refs, definitions))


# TODO move to parsers module


def parse_top_level_item_refs(items: dict[str, Any]) -> Iterator[str]:
    for prop_values in items.get("properties", {}).values():
        yield prop_values["$ref"]


def parse_definitions(definitions: dict[str, dict[str, Any]], top_level_refs: Iterable[str]) -> Iterator[Definition]:
    """
    Parse all definitions from the schema.

    Yield the top-level definitions first (to make the document more readable), then the rest.
    """
    top_level_titles = {Path(ref).name for ref in top_level_refs}
    other_than_top_level = []
    for def_values in definitions.values():
        definition = parse_definition(def_values)
        if definition.title in top_level_titles:
            yield definition
        else:
            other_than_top_level.append(definition)
    yield from other_than_top_level


def parse_definition(definition: dict[str, Any]) -> Definition:
    """Parse a single definition from the schema."""
    title = Path(definition["$id"]).name
    return Definition(
        title=title,
        description=definition.get("description", ""),
        type=definition.get("type", "–"),  # TODO: log a warning about missing type
        properties=definition.get("properties", {}),
        required_properties=definition.get("required", []),
    )


# TODO move to formatters module


def format_doc_content(main_item_refs: Iterable[str], definitions: Iterator[Definition]) -> Iterator[str]:
    """Format the documentation content to Markdown."""
    yield "# Valohai YAML Configuration Documentation\n"
    yield "## Top-level Properties\n"

    for ref in main_item_refs:
        yield f"- {_format_ref_link(ref)}"

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


def format_property(prop: dict[str, Any], parent_type: str | None = None, indentation_level: int = 1) -> Iterator[str]:
    """
    Format a single property to Markdown.

    - nested properties are formatted recursively
    - property types are added to the property name instead of listing them separately
    - parent type is used for special formatting rules (like "items" -> "array items")
    """
    indent = _get_indentation(indentation_level)
    for prop_name, prop_values in prop.items():
        if isinstance(prop_values, dict):
            formatted_name = _format_prop_name(prop_name, parent_type)
            prop_type = _get_type_definition(prop_values)
            if prop_type:
                formatted_name += f" *({prop_values.pop('type')})*"
            yield f"{indent}- {formatted_name}"
            yield from format_property(prop_values, parent_type=prop_type, indentation_level=indentation_level + 1)
        elif isinstance(prop_values, list):
            yield from _format_list_property(prop_name, prop_values, indentation_level)
        else:
            yield f"{indent}- {_format_atomic_property(prop_name, prop_values)}"


def _get_type_definition(prop_values: dict[str, Any]) -> str | None:
    """
    Get the type definition of a property, if it exists.

    Example: {"prop_name": {"type": "string"}} -> "string"
    """
    if "type" in prop_values and isinstance(prop_values["type"], str):
        return prop_values["type"]
    return None


def _has_type_definition(prop: Any) -> bool:
    """
    Check if a property has a type definition (that is not just another property called "type").

    Example: {"prop_name": {"type": "string"}} -> "prop_name" is of type "string"
    {"properties": {
      "type": { ... }
    }} -> "type" is a property itself, not a type definition
    """
    return isinstance(prop, dict) and "type" in prop and isinstance(prop["type"], str)


def _get_indentation(indentation_level: int) -> str:
    return "    " * indentation_level


def _format_prop_name(name: str, type: str | None) -> str:
    """
    Format a property name to Markdown, with some special rules.

    - custom properties in the actual YAML are monospaced
    - properties/items part of the schema itself are not (and are renamed for clarity)
    """
    if name == "items" and type == "array":
        return "array items"
    if name == "properties" and type == "object":
        return "object properties"
    return f"`{name}`"


def _format_list_property(name: str, values: list[Any], indentation_level: int = 1) -> Iterator[str]:
    """
    Format a list property to Markdown, with some special rules.

    - lists of values are formatted as a list of monospaced values.
    - values entered by the user in the actual YAML are monospaced
    - list values may be objects themselves -- continue recursively
    """
    indent = _get_indentation(indentation_level)
    if name == "enum":
        yield f"{indent}- allowed values: {' | '.join(sorted(f'`{v}`' for v in values))}"
    elif name == "required":
        yield f"{indent}- required properties: {', '.join(sorted(f'`{v}`' for v in values))}"
    else:
        yield f"{indent}- {name}"
        for list_item in values:
            yield from _format_list_value(list_item, indentation_level + 1)


def _format_list_value(item: Any, indentation_level: int) -> Iterator[str]:
    """Format list item to Markdown."""
    indent = _get_indentation(indentation_level)
    if isinstance(item, dict):
        # we have a list of objects here -- continue recursively with its values
        if _has_type_definition(item):
            # if the list items have a "type" definition, use that as the item name
            item_name = item.pop("type")
        elif ref := item.pop("$ref", None):
            # use ref links as item names
            item_name = _format_ref_link(ref)
        else:
            # just in case there are unhandled sub list types
            item_name = "(object)"
        yield f"{indent}- *{item_name}*"
        yield from format_property(item, indentation_level=indentation_level + 1)
    else:
        yield f"{indent}- {item}"


def _format_atomic_property(name: str, values: Any) -> str:
    """
    Format a single atomic property to Markdown, with some special rules.

    - values entered by the user in the actual YAML are monospaced
    - enum-type values are italicized
    """
    if name in ["additionalProperties", "type"]:
        return f"{name}: *{values}*"
    if name in ["const", "pattern"]:
        return f"{name}: `{values}`"
    if name == "$ref":
        return _format_ref_link(values)
    return f"{name}: {values}"


def _format_ref_link(ref: str) -> str:
    """Format a $ref link to Markdown."""
    ref_name = Path(ref).name
    return f"[`{ref_name}`](#{ref_name})"
