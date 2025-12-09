def test_serialize_step_parameter_with_widget(example1_config):
    config = example1_config
    parameters = config.steps["run training"].serialize()["parameters"]
    output_alias_param = next((param for param in parameters if param["name"] == "output-alias"), None)

    assert isinstance(output_alias_param, dict)
    assert output_alias_param["widget"]["type"] == "datumalias"
    assert output_alias_param["widget"]["settings"] == {"width": 123}


def test_serialize_workload_resources(step_with_resources):
    """Must not flatten workload resource data."""
    config = step_with_resources
    resources = config.steps["contains kubernetes resources"].serialize()["resources"]

    assert isinstance(resources, dict), "Resources should be defined."
    assert "cpu" in resources, "Resources should contain data."


def test_serialize_partial_resources(step_with_partial_resources):
    """Serialized data only contains keys found in the config."""
    config = step_with_partial_resources
    resources = config.steps["contains partial workload resources"].serialize()["resources"]

    assert "min" in resources["cpu"]
    assert "max" not in resources["cpu"]
