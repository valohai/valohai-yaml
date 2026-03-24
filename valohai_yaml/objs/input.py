from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Union

from valohai_yaml.objs.base import Item

if TYPE_CHECKING:
    from valohai_yaml.types import SerializedDict

KeepDirectoriesValue = Union[bool, str, "KeepDirectories"]


class KeepDirectories(Enum):
    """How to retain directories when using storage wildcards."""

    NONE = "none"
    SUFFIX = "suffix"
    FULL = "full"

    @classmethod
    def cast(cls, value: KeepDirectoriesValue) -> KeepDirectories:
        if isinstance(value, KeepDirectories):
            return value
        if not value:
            return KeepDirectories.NONE
        if value is True:
            return KeepDirectories.FULL
        return KeepDirectories(str(value).lower())


class DownloadIntent(Enum):
    """Specify input download intention."""

    ALWAYS = "always"
    ON_DEMAND = "on-demand"

    @classmethod
    def cast(cls, value: None | str | DownloadIntent) -> DownloadIntent:
        if isinstance(value, DownloadIntent):
            return value
        if value is None:
            return DownloadIntent.ALWAYS
        return DownloadIntent(str(value).lower())


class Input(Item):
    """Represents an input definition within a step definition."""

    def __init__(
        self,
        *,
        name: str,
        default: list[str] | str | None = None,
        optional: bool = False,
        description: str | None = None,
        keep_directories: KeepDirectoriesValue = False,
        filename: str | None = None,
        download: str | None = None,
    ) -> None:
        self.name = name
        self.default = default  # may be None, a string or a list of strings
        self.optional = bool(optional)
        self.description = description
        self.keep_directories = KeepDirectories.cast(keep_directories)
        self.filename = filename
        self.download = DownloadIntent.cast(download)

    def get_data(self) -> SerializedDict:
        data = super().get_data()
        if self.keep_directories is not KeepDirectories.NONE:
            data["keep_directories"] = data["keep_directories"].value
        else:
            data.pop("keep_directories", None)
        if self.download is not DownloadIntent.ALWAYS:
            data["download"] = data["download"].value
        else:
            data.pop("download", None)
        return data
