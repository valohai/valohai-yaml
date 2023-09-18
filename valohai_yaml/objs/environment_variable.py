from typing import Optional

from valohai_yaml.objs.base import Item


class EnvironmentVariable(Item):
    """An environment variable item (within executions)."""

    def __init__(
        self,
        *,
        name: str,
        default: Optional[str] = None,
        optional: bool = True,
        description: Optional[str] = None,
    ) -> None:
        self.name = name
        self.default = default  # may be None or a string
        self.optional = bool(optional)
        self.description = description
