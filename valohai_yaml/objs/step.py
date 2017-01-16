from __future__ import unicode_literals
from collections import OrderedDict

import six

from valohai_yaml.commands import build_command
from .base import _SimpleObject


class Parameter(_SimpleObject):
    pass


class Step(object):
    def __init__(self, name, image, command, parameters=(), inputs=(), outputs=()):
        self.name = name
        self.image = image
        self.command = command
        self.inputs = list(inputs)  # TODO: Improve handling
        self.outputs = list(outputs)  # TODO: Improve handling
        assert all(isinstance(p, Parameter) for p in parameters)
        self.parameters = OrderedDict((param.name, param) for param in parameters)

    @classmethod
    def parse(cls, data):
        kwargs = data.copy()
        kwargs['parameters'] = [Parameter(p_data) for p_data in kwargs.pop('parameters', ())]
        return cls(**kwargs)

    def serialize(self):
        val = {
            'name': self.name,
            'image': self.image,
            'command': self.command,
        }
        if self.parameters:
            val['parameters'] = list(p.serialize() for p in self.parameters.values())
        if self.inputs:
            val['inputs'] = self.inputs
        if self.outputs:
            val['outputs'] = self.outputs
        return val

    def get_parameter_defaults(self):
        """
        Get a dict mapping parameter names to their defaults (if set).
        :rtype: dict[str, object]
        """
        return {
            name: parameter.default
            for (name, parameter)
            in self.parameters.items()
            if ('default' in parameter)
            }

    def build_parameters(self, param_values):
        """
        Build the CLI command line from the given parameter values.

        :param param_values: mapping from parameter name to value
        :type param_values: dict[str, object]
        :return: list of CLI strings -- not escaped!
        :rtype: list[str]
        """
        param_bits = []
        for name, param in self.parameters.items():
            value = param_values.get(name)
            if value is None:
                continue
            pass_as_bits = six.text_type(param.get('pass-as', '--{name}={value}')).split()
            env = dict(param, value=value, v=value)
            param_bits.extend(bit.format(**env) for bit in pass_as_bits)
        return param_bits

    def build_command(self, parameter_values, command=None):
        """
        Build the command for this step using the given parameter values.

        Even if the original configuration only declared a single `command`,
        this function will return a list of shell commands.  It is the caller's
        responsibility to concatenate them, likely using the semicolon or
        double ampersands.

        It is also possible to override the `command`.

        :param parameter_values: Parameter values to augment any parameter defaults.
        :type parameter_values: dict[str, object]
        :param command: Overriding command; leave falsy to not override.
        :type command: str|list[str]|None
        :return: list of commands
        :rtype: list[str]
        """
        command = (command or self.command)
        # merge defaults with passed values
        values = dict(self.get_parameter_defaults(), **parameter_values)
        parameters = self.build_parameters(values)
        return build_command(command, parameters)
