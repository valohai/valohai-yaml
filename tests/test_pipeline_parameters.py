from valohai_yaml.objs import Pipeline


def test_programmatic_pipeline_parameters():
    parameterless_pipeline = Pipeline(name="...", nodes=[], edges=[])
    # Test that parameters aren't required
    assert parameterless_pipeline.parameters == []
    # Test that empty parameters are not serialized
    assert "parameters" not in parameterless_pipeline.serialize()
