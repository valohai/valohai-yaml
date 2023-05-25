from enum import Enum
from typing import List, Optional, Union

KeepDirectoriesValue = Union[bool, str, 'KeepDirectories']
ValueAtomType = Union[float, str, int, bool]
ValueType = Union[List[ValueAtomType], ValueAtomType]


class OverrideMode(Enum):
    """What should happen when error occurs in nodes execution."""

    MERGE = 'merge'  # merge inputs in a node with inputs from step
    OVERRIDE = 'override'  # default: override inputs in a node

    @classmethod
    def cast(cls, value: Optional[Union['OverrideMode', str]]) -> 'OverrideMode':
        if not value:
            return OverrideMode.OVERRIDE
        if isinstance(value, OverrideMode):
            return value
        value = str(value).lower()
        return OverrideMode(value)


class ErrorAction(Enum):
    """What should happen when error occurs in nodes execution."""

    STOP_ALL = 'stop-all'  # default: stop whole pipeline on error
    STOP_NEXT = 'stop-next'  # stop only following nodes on error
    CONTINUE = 'continue'  # continue pipeline as error never occurred

    @classmethod
    def cast(cls, value: Optional[Union['ErrorAction', str]]) -> 'ErrorAction':
        if not value:
            return ErrorAction.STOP_ALL
        if isinstance(value, ErrorAction):
            return value
        value = str(value).lower()
        if value == 'none':
            return ErrorAction.STOP_ALL
        return ErrorAction(value)


class KeepDirectories(Enum):
    """How to retain directories when using storage wildcards."""

    NONE = 'none'
    SUFFIX = 'suffix'
    FULL = 'full'

    @classmethod
    def cast(cls, value: KeepDirectoriesValue) -> 'KeepDirectories':
        if isinstance(value, KeepDirectories):
            return value
        if not value:
            return KeepDirectories.NONE
        if value is True:
            return KeepDirectories.FULL
        return KeepDirectories(str(value).lower())


class MultipleMode(Enum):
    """How to serialize multiple values given for a parameter."""

    SEPARATE = 'separate'
    REPEAT = 'repeat'

    @classmethod
    def cast(cls, value: Optional[Union['MultipleMode', str]]) -> Optional['MultipleMode']:
        if not value:
            return None
        if isinstance(value, MultipleMode):
            return value
        value = str(value).lower()
        if value == 'none':
            return None
        return MultipleMode(value)
