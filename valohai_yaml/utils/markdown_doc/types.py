from typing import Any, NamedTuple


class Definition(NamedTuple):
    """YAML configuration definition item."""

    title: str
    description: str
    type: str
    properties: dict[str, dict[str, Any]]
    required_properties: list[str]
