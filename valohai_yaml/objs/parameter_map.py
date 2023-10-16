from typing import List, Mapping, Optional

from valohai_yaml.objs.parameter import Parameter, ValueType


class ParameterMap:
    """Container for an execution's parameters and the values assigned."""

    def __init__(
        self,
        *,
        parameters: Mapping[str, Parameter],
        values: Mapping[str, Optional[ValueType]],
    ) -> None:
        self.parameters = parameters
        self.values = values

    def build_parameters(self) -> List[str]:
        """
        Build the CLI command line from the parameter values. Omit parameters with None value.

        :return: list of CLI strings -- not escaped!
        """
        param_bits = []
        for name in self.parameters:
            param_bits.extend(self.build_parameter_by_name(name) or [])
        return param_bits

    def build_parameter_by_name(self, name: str) -> Optional[List[str]]:
        param = self.parameters[name]
        value = self.values.get(param.name)
        if value is None:
            return None
        return param.format_cli(value)
