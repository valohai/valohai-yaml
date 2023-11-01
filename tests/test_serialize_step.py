def test_serialize_workload_resources(step_with_resources):
    """Must not flatten workload resource data."""
    config = step_with_resources
    resources = config.steps["contains kubernetes resources"].resources

    assert isinstance(resources, dict), "Resources should be defined."
    assert "cpu" in resources, "Resources should contain data."


def test_serialize_partial_resources(step_with_partial_resources):
    """Serialized data only contains keys found in the config."""
    config = step_with_partial_resources
    resources = config.steps["contains partial workload resources"].resources

    assert "min" in resources["cpu"]
    assert "max" not in resources["cpu"]
