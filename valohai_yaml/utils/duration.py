import datetime
import re
from typing import Optional, Union

suffixes = {
    "s": 1,
    "m": 60,
    "h": 60 * 60,
    "d": 60 * 60 * 24,
    "w": 60 * 60 * 24 * 7,
}

simple_duration_re = re.compile(r"(?P<value>[.\d]+)\s*(?P<suffix>[a-z]*)")


def parse_duration_string(duration_str: str) -> datetime.timedelta:
    total_duration_sec = 0.0
    for match in simple_duration_re.finditer(duration_str):
        value = float(match.group("value"))
        suffix = match.group("suffix").lower()
        if suffix[0] not in suffixes:
            raise ValueError(f"Unknown duration suffix in {match.group(0)!r}")
        total_duration_sec += value * suffixes[suffix[0]]
    if total_duration_sec <= 0:
        raise ValueError(f"Could not parse positive duration from {duration_str!r}")
    return datetime.timedelta(seconds=total_duration_sec)


def parse_duration(
    duration_value: Union[int, str, None],
) -> Optional[datetime.timedelta]:
    if duration_value is None:
        return None
    if isinstance(duration_value, int):
        return datetime.timedelta(seconds=duration_value)
    if isinstance(duration_value, str):
        if duration_value.strip():
            return parse_duration_string(duration_value)
        return None
    raise ValueError(f"Could not parse duration from {duration_value!r}")
