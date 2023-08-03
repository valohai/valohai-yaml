import copy
import datetime
from collections import OrderedDict
from typing import Any, Dict, Iterable, List, Optional, Union

from valohai_yaml.commands import build_command
from valohai_yaml.lint import LintResult
from valohai_yaml.objs.base import Item
from valohai_yaml.objs.environment_variable import EnvironmentVariable
from valohai_yaml.objs.input import Input
from valohai_yaml.objs.mount import Mount
from valohai_yaml.objs.parameter import Parameter
from valohai_yaml.objs.parameter_map import ParameterMap
from valohai_yaml.objs.utils import (
    check_type_and_dictify,
    check_type_and_listify,
    consume_array_of,
    serialize_into,
)
from valohai_yaml.types import LintContext, SerializedDict
from valohai_yaml.utils.duration import parse_duration
from valohai_yaml.utils.lint import lint_iterables
from valohai_yaml.utils.merge import merge_dicts, merge_simple


class Step(Item):
    """Represents an execution step definition."""

    def __init__(
        self,
        *,
        name: str,
        image: str,
        command: Union[List[str], str],
        parameters: Iterable[Parameter] = (),
        inputs: Iterable[Input] = (),
        outputs: Iterable[Any] = (),
        mounts: Iterable[Mount] = (),
        environment_variables: Iterable[EnvironmentVariable] = (),
        environment: Optional[str] = None,
        description: Optional[str] = None,
        time_limit: Optional[datetime.timedelta] = None,
        no_output_timeout: Optional[datetime.timedelta] = None,
        icon: Optional[str] = None,
        category: Optional[str] = None,
    ) -> None:
        self.name = name
        self.image = image
        self.command = command
        self.description = description
        self.environment = (str(environment) if environment else None)
        self.icon = (str(icon) if icon else None)
        self.category = (str(category) if category else None)

        self.outputs = list(outputs)  # TODO: Improve handling
        self.mounts = check_type_and_listify(mounts, Mount)
        self.inputs = check_type_and_dictify(inputs, Input, 'name')
        self.parameters = check_type_and_dictify(parameters, Parameter, 'name')
        self.environment_variables = check_type_and_dictify(environment_variables, EnvironmentVariable, 'name')

        self.time_limit = time_limit
        self.no_output_timeout = no_output_timeout

    @classmethod
    def parse(cls, data: SerializedDict) -> 'Step':
        kwargs = parse_common_step_properties(data)
        kwargs['time_limit'] = parse_duration(kwargs.pop('time-limit', None))
        kwargs['no_output_timeout'] = parse_duration(kwargs.pop('no-output-timeout', None))
        inst = cls(**kwargs)
        inst._original_data = data
        return inst

    def serialize(self) -> OrderedDict:  # type: ignore[type-arg]
        val = OrderedDict([
            ('name', self.name),
            ('image', self.image),
            ('command', self.command),
        ])
        for key, source in [
            ('parameters', self.parameters),
            ('inputs', self.inputs),
            ('mounts', self.mounts),
            ('outputs', self.outputs),
            ('environment', self.environment),
            ('environment-variables', self.environment_variables),
            ('description', self.description),
            ('time-limit', int(self.time_limit.total_seconds()) if self.time_limit else None),
            ('no-output-timeout', int(self.no_output_timeout.total_seconds()) if self.no_output_timeout else None),
            ('icon', self.icon),
            ('category', self.category),
        ]:
            serialize_into(val, key, source, flatten_dicts=True, elide_empty_iterables=True)
        return val

    def get_parameter_defaults(self, include_flags: bool = True) -> Dict[str, Any]:
        """Get a dict mapping parameter names to their defaults (if set)."""
        return {
            name: parameter.default
            for (name, parameter)
            in self.parameters.items()
            if parameter.default is not None and (include_flags or parameter.type != 'flag')
        }

    def build_command(
        self,
        parameter_values: Dict[str, Any],
        command: Optional[Union[List[str], str]] = None
    ) -> List[str]:
        """
        Build the command for this step using the given parameter values.

        Even if the original configuration only declared a single `command`,
        this function will return a list of shell commands.  It is the caller's
        responsibility to concatenate them, likely using the semicolon or
        double ampersands.

        It is also possible to override the `command`.

        :param parameter_values: Parameter values to augment any parameter defaults.
        :param command: Overriding command; leave falsy to not override.
        :return: list of commands
        """
        command = (command or self.command)

        # merge defaults with passed values
        # ignore flag default values as they are special
        # undefined flag will remain undefined regardless of default value
        values = dict(self.get_parameter_defaults(include_flags=False), **parameter_values)

        parameter_map = ParameterMap(parameters=self.parameters, values=values)
        return build_command(command, parameter_map)

    def lint(self, lint_result: LintResult, context: LintContext) -> None:
        context = dict(context, step=self)

        lint_iterables(lint_result, context, (
            self.parameters,
            self.inputs,
            self.mounts,
            self.environment_variables,
            self.outputs,
        ))

    @classmethod
    def default_merge(cls, a: 'Step', b: 'Step') -> 'Step':
        result = merge_simple(a, b)
        result.parameters = merge_dicts(
            a.parameters,
            b.parameters,
            merger=merge_simple,
            copier=copy.deepcopy,
        )
        result.inputs = merge_dicts(
            a.inputs,
            b.inputs,
            merger=merge_simple,
            copier=copy.deepcopy,
        )
        result.outputs = a.outputs[:] + b.outputs[:]  # TODO: Improve handling
        result.environment_variables = merge_dicts(
            a.environment_variables,
            b.environment_variables,
            merger=merge_simple,
            copier=copy.deepcopy,
        )
        return result


def parse_common_step_properties(data: SerializedDict) -> Dict[str, Any]:
    """Parse common properties in step and override objects."""
    kwargs = data.copy()
    kwargs['parameters'] = consume_array_of(kwargs, 'parameters', Parameter)
    kwargs['inputs'] = consume_array_of(kwargs, 'inputs', Input)
    kwargs['mounts'] = consume_array_of(kwargs, 'mounts', Mount)
    kwargs['environment_variables'] = consume_array_of(kwargs, 'environment-variables', EnvironmentVariable)
    return kwargs
