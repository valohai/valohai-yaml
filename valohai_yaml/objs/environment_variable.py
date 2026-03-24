from __future__ import annotations

from valohai_yaml.objs.base import Item


class EnvironmentVariable(Item):
    """An environment variable item (within executions)."""

    def __init__(
        self,
        *,
        name: str,
        default: str | None = None,
        optional: bool = True,
        description: str | None = None,
    ) -> None:
        self.name = name
        self.default = default  # may be None or a string
        self.optional = bool(optional)
        self.description = description
