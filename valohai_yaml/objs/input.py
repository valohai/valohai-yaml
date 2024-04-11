from copy import copy
from enum import Enum
from typing import List, Optional, Union

from valohai_yaml.objs.base import Item
from valohai_yaml.types import SerializedDict

KeepDirectoriesValue = Union[bool, str, "KeepDirectories"]
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
            return EdgeMergeMode.APPEND
        return EdgeMergeMode(str(value).lower())


class KeepDirectories(Enum):
    """How to retain directories when using storage wildcards."""

    NONE = "none"
    SUFFIX = "suffix"
    FULL = "full"

    @classmethod
    def cast(cls, value: KeepDirectoriesValue) -> "KeepDirectories":
        if isinstance(value, KeepDirectories):
            return value
        if not value:
            return KeepDirectories.NONE
        if value is True:
            return KeepDirectories.FULL
        return KeepDirectories(str(value).lower())


class Input(Item):
    """Represents an input definition within a step definition."""

    def __init__(
        self,
        *,
        name: str,
        default: Optional[Union[List[str], str]] = None,
        optional: bool = False,
        description: Optional[str] = None,
        keep_directories: KeepDirectoriesValue = False,
        filename: Optional[str] = None,
        edge_merge_mode: EdgeMergeMode = EdgeMergeMode.REPLACE,
    ) -> None:
        self.name = name
        self.default = default  # may be None, a string or a list of strings
        self.optional = bool(optional)
        self.description = description
        self.keep_directories = KeepDirectories.cast(keep_directories)
        self.filename = filename
        self.edge_merge_mode = EdgeMergeMode.cast(edge_merge_mode)

    def get_data(self) -> SerializedDict:
        data = super().get_data()
        if self.keep_directories is not KeepDirectories.NONE:
            data["keep_directories"] = data["keep_directories"].value
        else:
            data.pop("keep_directories", None)
        return data

    def with_edge_merge_mode_applied(self) -> "Input":
        new_input = copy(self)
        if new_input.edge_merge_mode == EdgeMergeMode.REPLACE:
            new_input.default = []
        return new_input
