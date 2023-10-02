import pytest

from valohai_yaml.objs import Pipeline, PipelineParameter


def test_programmatic_pipeline_parameters():
    parameterless_pipeline = Pipeline(name="...", nodes=[], edges=[])
    # Test that parameters aren't required
    assert parameterless_pipeline.parameters == []
    # Test that empty parameters are not serialized
    assert "parameters" not in parameterless_pipeline.serialize()


def test_pipeline_parameters(pipeline_with_parameters_config):
    pipe = pipeline_with_parameters_config.pipelines["Example Pipeline with Parameters"]
    assert len(pipe.parameters) > 0
    param = next(param for param in pipe.parameters if param.name == "id")
    assert isinstance(param, PipelineParameter)
    assert param.targets == [
        "train.parameter.id",
        "train_parallel.parameter.id",
    ]


@pytest.mark.parametrize(
    "name",
    ("Short hand parameter target", "Short hand parameter target 2"),
)
def test_pipeline_parameter_shorthand(pipeline_with_parameters_config, name):
    pipe = pipeline_with_parameters_config.pipelines[name]
    assert len(pipe.parameters) > 0
    param = next(param for param in pipe.parameters if param.name == "id")
    assert isinstance(param, PipelineParameter)
    assert param.name == "id"
    assert param.targets == ["train.parameter.id"]
