from __future__ import unicode_literals

import re
import warnings

from valohai_yaml.objs.parameter_map import LegacyParameterMap
from valohai_yaml.utils import listify

try:
    from shlex import quote
except ImportError:  # pragma: no cover
    from pipes import quote


class CommandInterpolationWarning(UserWarning):
    pass


interpolable_re = re.compile(r'{(.+?)}')


def quote_multiple(args):
    if not args:
        return ''
    return ' '.join(quote(arg) for arg in args)


def _replace_interpolation(parameter_map, match):
    value = match.group(1)
    if value in ('parameters', 'params'):
        return quote_multiple(parameter_map.build_parameters())
    elif value.startswith('parameter:'):
        parameter_name = value.split(':', 1)[1]
        if parameter_name in parameter_map.parameters:
            return quote_multiple(parameter_map.build_parameter_by_name(parameter_name))
    elif value.startswith('parameter-value:'):
        parameter_name = value.split(':', 1)[1]
        value = parameter_map.values.get(parameter_name)
        if value:
            return quote(value)
    return match.group(0)  # Return the original otherwise


def build_command(command, parameter_map):
    """
    Build command line(s) using the given parameter map.

    Even if the passed a single `command`, this function will return a list
    of shell commands.  It is the caller's responsibility to concatenate them,
    likely using the semicolon or double ampersands.

    :param command: The command to interpolate params into.
    :type command: str|list[str]
    :param parameter_map: A ParameterMap object containing parameter knowledge.
    :type parameter_map: valohai_yaml.objs.parameter_map.ParameterMap

    :return: list of commands
    :rtype: list[str]
    """

    if isinstance(parameter_map, list):  # Partially emulate old (pre-0.7) API for this function.
        parameter_map = LegacyParameterMap(parameter_map)

    out_commands = []
    for command in listify(command):
        # Only attempt formatting if the string smells like it should be formatted.
        # This allows the user to include shell syntax in the commands, if required.
        # (There's still naturally the chance for false-positives, so guard against
        #  those value errors and warn about them.)

        if interpolable_re.search(command):
            try:
                command = interpolable_re.sub(
                    lambda match: _replace_interpolation(parameter_map, match),
                    command,
                )
            except ValueError as exc:  # pragma: no cover
                warnings.warn(
                    'failed to interpolate into %r: %s' % (command, exc),
                    CommandInterpolationWarning
                )
        out_commands.append(command.strip())
    return out_commands
