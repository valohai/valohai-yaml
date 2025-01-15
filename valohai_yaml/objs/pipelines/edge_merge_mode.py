from enum import Enum
from typing import Union

EdgeMergeModeValue = Union[str, "EdgeMergeMode"]


class EdgeMergeMode(Enum):
    """Input override mode."""

    REPLACE = "replace"
    APPEND = "append"

    @classmethod
    def cast(cls, value: EdgeMergeModeValue) -> "EdgeMergeMode":
        if isinstance(value, EdgeMergeMode):
            return value
        if not value:
            return DEFAULT_EDGE_MERGE_MODE
        return EdgeMergeMode(str(value).lower())


DEFAULT_EDGE_MERGE_MODE = EdgeMergeMode.REPLACE
