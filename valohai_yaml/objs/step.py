from __future__ import unicode_literals

from collections import OrderedDict

from valohai_yaml.commands import build_command
from valohai_yaml.utils.lint import lint_iterables
from .base import Item
from .environment_variable import EnvironmentVariable
from .parameter_map import ParameterMap
from .utils import consume_array_of, serialize_into
from .input import Input
from .mount import Mount
from .parameter import Parameter


class Step(Item):

    def __init__(
        self,
        name,
        image,
        command,
        parameters=(),
        inputs=(),
        outputs=(),
        mounts=(),
        environment_variables=(),
        environment=None,
        description=None,
    ):
        self.name = name
        self.image = image
        self.command = command
        self.description = description

        self.outputs = list(outputs)  # TODO: Improve handling

        assert all(isinstance(m, Mount) for m in mounts)
        self.mounts = list(mounts)

        assert all(isinstance(i, Input) for i in inputs)
        self.inputs = OrderedDict((input.name, input) for input in inputs)

        assert all(isinstance(p, Parameter) for p in parameters)
        self.parameters = OrderedDict((param.name, param) for param in parameters)

        self.environment_variables = OrderedDict((ev.name, ev) for ev in environment_variables)
        self.environment = (str(environment) if environment else None)

    @classmethod
    def parse(cls, data):
        kwargs = data.copy()
        kwargs['parameters'] = consume_array_of(kwargs, 'parameters', Parameter)
        kwargs['inputs'] = consume_array_of(kwargs, 'inputs', Input)
        kwargs['mounts'] = consume_array_of(kwargs, 'mounts', Mount)
        kwargs['environment_variables'] = consume_array_of(kwargs, 'environment-variables', EnvironmentVariable)
        inst = cls(**kwargs)
        inst._original_data = data
        return inst

    def serialize(self):
        val = {
            'name': self.name,
            'image': self.image,
            'command': self.command,
        }
        for key, source in [
            ('parameters', self.parameters),
            ('inputs', self.inputs),
            ('mounts', self.mounts),
            ('outputs', self.outputs),
            ('environment', self.environment),
            ('environment-variables', self.environment_variables),
            ('description', self.description),
        ]:
            serialize_into(val, key, source, flatten_dicts=True, elide_empty_iterables=True)
        return val

    def get_parameter_defaults(self, include_flags=True):
        """
        Get a dict mapping parameter names to their defaults (if set).
        :rtype: dict[str, object]
        """
        return {
            name: parameter.default
            for (name, parameter)
            in self.parameters.items()
            if parameter.default is not None and (include_flags or parameter.type != 'flag')
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
        # ignore flag default values as they are special
        # undefined flag will remain undefined regardless of default value
        values = dict(self.get_parameter_defaults(include_flags=False), **parameter_values)

        parameter_map = ParameterMap(parameters=self.parameters, values=values)
        return build_command(command, parameter_map)

    def lint(self, lint_result, context):
        context = dict(context, step=self)

        lint_iterables(lint_result, context, (
            self.parameters,
            self.inputs,
            self.mounts,
            self.environment_variables,
            self.outputs,
        ))
