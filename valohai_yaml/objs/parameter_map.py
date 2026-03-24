from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping

    from valohai_yaml.objs.parameter import Parameter, ValueType


class ParameterMap:
    """Container for an execution's parameters and the values assigned."""

    def __init__(
        self,
        *,
        parameters: Mapping[str, Parameter],
        values: Mapping[str, ValueType | None],
    ) -> None:
        self.parameters = parameters
        self.values = values

    def build_parameters(self) -> list[str]:
        """
        Build the CLI command line from the parameter values. Omit parameters with None value.

        :return: list of CLI strings -- not escaped!
        """
        param_bits = []
        for name in self.parameters:
            param_bits.extend(self.build_parameter_by_name(name) or [])
        return param_bits

    def build_parameter_by_name(self, name: str) -> list[str] | None:
        param = self.parameters[name]
        value = self.values.get(param.name)
        if value is None:
            return None
        return param.format_cli(value)
