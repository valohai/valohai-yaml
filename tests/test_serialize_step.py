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


def test_serialize_autorestart(step_with_autorestart):
    """Serialized data contains autorestart only when it is set in the config."""
    steps = step_with_autorestart.steps

    assert steps["autorestarting step"].serialize()["autorestart"] is True
    assert steps["non-autorestarting step"].serialize()["autorestart"] is False
    assert "autorestart" not in steps["autorestart-agnostic step"].serialize()


def test_serialize_preset(step_with_preset):
    """Serialized data contains preset ID."""
    config = step_with_preset
    preset = config.steps["preset-id step"].serialize()["runtime-config-preset"]

    assert preset == "preset-1234", "Preset ID should be serialized correctly."
