import re
import warnings
from shlex import quote
from typing import TYPE_CHECKING, Dict, List, Optional, Union

from valohai_yaml.objs.parameter_map import ParameterMap
from valohai_yaml.utils import listify

if TYPE_CHECKING:
    from re import Match


class CommandInterpolationWarning(UserWarning):
    """Warning issued when command interpolation fails."""


interpolable_re = re.compile(r"{(.+?)}")


def quote_multiple(args: Optional[List[str]]) -> str:
    if not args:
        return ""
    return " ".join(quote(arg) for arg in args)


def _replace_interpolation(
    parameter_map: ParameterMap,
    match: "Match[str]",
    special_interpolations: Dict[str, str],
) -> str:
    value = match.group(1)

    if value in special_interpolations:
        return quote(special_interpolations[value])

    if value in ("parameters", "params"):
        return quote_multiple(parameter_map.build_parameters())

    if value.startswith("parameter:"):
        parameter_name = value.split(":", 1)[1]
        if parameter_name in parameter_map.parameters:
            return quote_multiple(parameter_map.build_parameter_by_name(parameter_name))

    if value.startswith("parameter-value:"):
        parameter_name = value.split(":", 1)[1]
        if parameter_name in parameter_map.values:
            return quote(str(parameter_map.values[parameter_name]))
    return match.group(0)  # Return the original otherwise


def build_command(
    command: Union[str, List[str]],
    parameter_map: ParameterMap,
    special_interpolations: Optional[Dict[str, str]] = None,
) -> List[str]:
    """
    Build command line(s) using the given parameter map.

    Even if passed a single `command`, this function will return a list
    of shell commands.  It is the caller's responsibility to concatenate them,
    likely using the semicolon or double ampersands. The `join_command` function
    can be used for this purpose.

    :param command: The command to interpolate params into.
    :param parameter_map: A ParameterMap object containing parameter knowledge.
    :param special_interpolations: a str-str dict containing special interpolations

    :return: list of commands
    """
    if isinstance(parameter_map, list):
        raise TypeError("Passing in lists as ParameterMaps is no longer supported.")

    special: Dict[str, str]
    special = {} if special_interpolations is None else special_interpolations

    out_commands = []
    commands: List[str] = listify(command)
    for command in commands:
        # Only attempt formatting if the string smells like it should be formatted.
        # This allows the user to include shell syntax in the commands, if required.
        # (There's still naturally the chance for false-positives, so guard against
        #  those value errors and warn about them.)

        if interpolable_re.search(command):
            try:
                command = interpolable_re.sub(
                    lambda match: _replace_interpolation(parameter_map, match, special),
                    command,
                )
            except ValueError as exc:  # pragma: no cover
                warnings.warn(
                    f"failed to interpolate into {command!r}: {exc}",
                    CommandInterpolationWarning,
                    stacklevel=2,
                )
        out_commands.append(command.strip())
    return out_commands


def join_command(commands: List[str], joiner: str) -> str:
    """
    Join a list of commands into a single "script" that could be run using e.g. `sh -c`.

    The commands (if not empty or purely whitespace)
    are joined using the given joiner, but care is taken
    to ensure that a shebang line, if any present at the start of the
    first command, is preserved as a line of its own, as expected for
    a script. (Note that `sh -c` wouldn't interpret it as a shebang line.)

    :param commands: List of command pieces, e.g. from `build_command`.
    :return: Single script string
    """
    shebang_line = None
    bits = []
    for i, cmd in enumerate(commands):
        if i == 0 and cmd.startswith("#!"):
            shebang_line, _, cmd = cmd.partition("\n")
        if not cmd.strip():
            continue
        bits.append(cmd)
    joined_bits = joiner.join(bits)
    if shebang_line:
        return f"{shebang_line}\n{joined_bits}"
    return joined_bits
