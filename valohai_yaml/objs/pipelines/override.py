from __future__ import annotations

import copy
from collections import OrderedDict
from typing import Iterable

from valohai_yaml.objs import Mount, Parameter
from valohai_yaml.objs.base import Item
from valohai_yaml.objs.environment_variable import EnvironmentVariable
from valohai_yaml.objs.input import Input
from valohai_yaml.objs.step import Step, parse_common_step_properties
from valohai_yaml.objs.utils import (
    check_type_and_dictify,
    check_type_and_listify,
    serialize_into,
)
from valohai_yaml.types import SerializedDict
from valohai_yaml.utils import listify
from valohai_yaml.utils.merge import merge_dicts, merge_simple


class Override(Item):
    """Represents the step fields overridden in an execution or task node."""

    def __init__(
        self,
        *,
        image: str | None = None,
        command: list[str] | str | None = None,
        parameters: Iterable[Parameter] | None = None,
        inputs: Iterable[Input] | None = None,
        mounts: Iterable[Mount] | None = None,
        environment_variables: Iterable[EnvironmentVariable] | None = None,
        environment: str | None = None,
    ) -> None:
        self.image = image
        self.command = command
        self.environment = str(environment) if environment else None
        self.mounts = check_type_and_listify(mounts, Mount)
        self.inputs = check_type_and_dictify(inputs, Input, "name")
        self.parameters = check_type_and_dictify(parameters, Parameter, "name")
        self.environment_variables = check_type_and_dictify(
            environment_variables,
            EnvironmentVariable,
            "name",
        )

    @classmethod
    def merge_with_step(cls, a: Override | None, step: Step) -> Override:
        """Merge an override with a step, returning a new override object."""
        override = copy.deepcopy(a) if a else cls()
        override.parameters = merge_dicts(
            step.parameters,
            override.parameters,
            merger=merge_simple,
            copier=copy.deepcopy,
        )
        override.inputs = merge_dicts(
            step.inputs,
            override.inputs,
            merger=merge_simple,
            copier=copy.deepcopy,
        )
        override.environment_variables = merge_dicts(
            step.environment_variables,
            override.environment_variables,
            merger=merge_simple,
            copier=copy.deepcopy,
        )
        return override

    @classmethod
    def serialize_to_template(cls, override: Override) -> OrderedDict:
        """Serialize an override object to a template for a node."""
        template = override.serialize()
        template["inputs"] = {
            name: listify(input.default)
            for name, input in override.inputs.items()
        }
        template["parameters"] = {
            name: param.default
            for name, param in override.parameters.items()
        }
        return template

    @classmethod
    def parse(cls, data: SerializedDict) -> Override:
        kwargs = parse_common_step_properties(data)
        inst = cls(**kwargs)
        inst._original_data = data
        return inst

    def serialize(self) -> OrderedDict:  # type: ignore[type-arg]
        val: OrderedDict = OrderedDict()
        for key, source in [
            ("image", self.image),
            ("command", self.command),
            ("parameters", self.parameters),
            ("inputs", self.inputs),
            ("mounts", self.mounts),
            ("environment", self.environment),
            ("environment-variables", self.environment_variables),
        ]:
            if source:
                serialize_into(
                    val,
                    key,
                    source,
                    flatten_dicts=True,
                    elide_empty_iterables=True,
                )
        return val
