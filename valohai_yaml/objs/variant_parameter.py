from __future__ import annotations

from enum import Enum
from typing import Any

from valohai_yaml.objs.base import Item


class VariantParameterStyle(Enum):
    """Represents a variant parameter style definition."""

    LOGSPACE = "logspace"
    MULTIPLE = "multiple"
    LINEAR = "linear"
    SINGLE = "single"
    RANDOM = "random"

    @classmethod
    def cast(cls, value: VariantParameterStyle | str | None) -> VariantParameterStyle:
        if not value:
            return VariantParameterStyle.SINGLE
        if isinstance(value, VariantParameterStyle):
            return value
        value = str(value).lower()
        return VariantParameterStyle(value)


class VariantParameter(Item):
    """Represents a variant parameter definition."""

    rules: dict[str, Any]
    name: str
    style: VariantParameterStyle

    def __init__(
        self,
        *,
        rules: dict[str, Any],
        name: str,
        style: VariantParameterStyle | str,
    ) -> None:
        self.rules = rules
        self.name = name
        self.style = VariantParameterStyle.cast(style)
