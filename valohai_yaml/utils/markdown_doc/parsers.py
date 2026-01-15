from pathlib import Path
from typing import Any, Iterable, Iterator

from valohai_yaml.utils.markdown_doc.types import Definition


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
    type = definition.get("type")

    # check for anyOf definitions on the main level --
    # these don't have normal property keys, just the anyOf list
    if not type and "anyOf" in definition:
        return Definition(
            title=title,
            description=definition.get("description", ""),
            type="anyOf",
            properties={"anyOf": definition.get("anyOf", [])},
            required_properties=[],
        )

    return Definition(
        title=title,
        description=definition.get("description", ""),
        type=type or "–",
        properties=definition.get("properties", {}),
        required_properties=definition.get("required", []),
    )
