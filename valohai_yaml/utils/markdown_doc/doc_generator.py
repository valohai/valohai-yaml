from typing import Any

from valohai_yaml.utils.markdown_doc.formatters import format_doc_content
from valohai_yaml.utils.markdown_doc.parsers import parse_definitions, parse_top_level_item_refs


def generate_schema_doc(schema_dict: dict[str, Any]) -> str:
    """
    Generate JSONSchema documentation in Markdown format.

    Based on the configuration JSON schema.
    """
    top_level_item_refs = list(parse_top_level_item_refs(schema_dict.get("items", {})))
    definitions = parse_definitions(schema_dict.get("$defs", {}), top_level_item_refs)

    return "\n".join(format_doc_content(top_level_item_refs, definitions))
