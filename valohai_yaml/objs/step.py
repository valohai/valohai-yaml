from __future__ import unicode_literals

from collections import OrderedDict

from valohai_yaml.commands import build_command
from valohai_yaml.objs.parameter_map import ParameterMap

from .input import Input
from .mount import Mount
from .parameter import Parameter


class Step(object):

    def __init__(self, name, image, command, parameters=(), inputs=(), outputs=(), mounts=()):
        self.name = name
        self.image = image
        self.command = command

        self.outputs = list(outputs)  # TODO: Improve handling

        assert all(isinstance(m, Mount) for m in mounts)
        self.mounts = list(mounts)

        assert all(isinstance(i, Input) for i in inputs)
        self.inputs = OrderedDict((input.name, input) for input in inputs)

        assert all(isinstance(p, Parameter) for p in parameters)
        self.parameters = OrderedDict((param.name, param) for param in parameters)

    @classmethod
    def parse(cls, data):
        kwargs = data.copy()
        kwargs['parameters'] = [Parameter.parse(p_data) for p_data in kwargs.pop('parameters', ())]
        kwargs['inputs'] = [Input.parse(i_data) for i_data in kwargs.pop('inputs', ())]
        kwargs['mounts'] = [Mount.parse(m_data) for m_data in kwargs.pop('mounts', ())]
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
            val['inputs'] = list(i.serialize() for i in self.inputs.values())
        if self.mounts:
            val['mounts'] = [m.serialize() for m in self.mounts]
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
            if parameter.default is not None
        }

    def build_parameters(self, param_values):  # pragma: no cover
        # TODO: Legacy; no longer used internally. Remove at 1.0.
        return ParameterMap(self.parameters, param_values).build_parameters()

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
        parameter_map = ParameterMap(parameters=self.parameters, values=values)
        return build_command(command, parameter_map)
