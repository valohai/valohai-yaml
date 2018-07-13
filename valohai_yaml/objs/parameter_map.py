class ParameterMap:
    def __init__(self, parameters, values):
        self.parameters = parameters
        self.values = values

    def build_parameters(self):
        """
        Build the CLI command line from the parameter values.

        :return: list of CLI strings -- not escaped!
        :rtype: list[str]
        """
        param_bits = []
        for name in self.parameters:
            param_bits.extend(self.build_parameter_by_name(name) or [])
        return param_bits

    def build_parameter_by_name(self, name):
        param = self.parameters[name]
        value = self.values.get(param.name)
        return param.format_cli(value)


class LegacyParameterMap:
    def __init__(self, parameters_list):
        self.parameters_list = parameters_list
        self.parameters = {}
        self.values = {}

    def build_parameters(self):
        return self.parameters_list[:]

    def build_parameter_by_name(self, name):  # pragma: no cover
        return None
