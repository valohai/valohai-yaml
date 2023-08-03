from __future__ import annotations

from collections import OrderedDict
from typing import Iterable

from valohai_yaml.objs import Mount, Parameter
from valohai_yaml.objs.base import Item
from valohai_yaml.objs.environment_variable import EnvironmentVariable
from valohai_yaml.objs.input import Input
from valohai_yaml.objs.step import parse_common_step_properties
from valohai_yaml.objs.utils import (
    check_type_and_dictify,
    check_type_and_listify,
    serialize_into,
)
from valohai_yaml.types import SerializedDict


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
