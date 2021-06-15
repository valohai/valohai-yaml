from typing import Dict, List, Optional

from .parameter import Parameter


class ParameterMap:
    """Container for an execution's parameters and the values assigned."""

    def __init__(self, *, parameters: Dict[str, Parameter], values) -> None:
        self.parameters = parameters
        self.values = values

    def build_parameters(self) -> List[str]:
        """
        Build the CLI command line from the parameter values.

        :return: list of CLI strings -- not escaped!
        :rtype: list[str]
        """
        param_bits = []
        for name in self.parameters:
            param_bits.extend(self.build_parameter_by_name(name) or [])
        return param_bits

    def build_parameter_by_name(self, name: str) -> Optional[List[str]]:
        param = self.parameters[name]
        value = self.values.get(param.name)
        return param.format_cli(value)
