from __future__ import unicode_literals
import warnings

try:
    from shlex import quote
except ImportError:  # pragma: no cover
    from pipes import quote

from valohai_yaml.utils import listify


class CommandInterpolationWarning(UserWarning):
    pass


def build_command(command, parameters):
    """
    Build command line(s) using the given parameter values.

    Even if the passed a single `command`, this function will return a list
    of shell commands.  It is the caller's responsibility to concatenate them,
    likely using the semicolon or double ampersands.

    :param command: The command to interpolate params into.
    :type command: str|list[str]
    :param parameter_values: Command line parameters for the {parameters} placeholder.
                             These are quoted within `build_command`.
    :type parameter_values: list[str]

    :return: list of commands
    :rtype: list[str]
    """
    parameters_str = ' '.join(quote(parameter) for parameter in parameters)
    # format each command
    env = dict(parameters=parameters_str, params=parameters_str)
    out_commands = []
    for command in listify(command):
        # Only attempt formatting if the string smells like it should be formatted.
        # This allows the user to include shell syntax in the commands, if required.
        # (There's still naturally the chance for false-positives, so guard against
        #  those value errors and warn about them.)

        if any('{%s}' % key in command for key in env):
            try:
                command = command.format(**env)
            except ValueError as exc:  # pragma: no cover
                warnings.warn(
                    'failed to interpolate parameters into %r: %s' % (command, exc),
                    CommandInterpolationWarning
                )
        out_commands.append(command)
    return out_commands
