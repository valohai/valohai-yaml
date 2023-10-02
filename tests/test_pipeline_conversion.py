from valohai_yaml.objs import Config
from valohai_yaml.pipelines.conversion import PipelineConverter
from valohai_yaml.utils.duration import parse_duration_string


def test_pipeline_conversion_smoke(pipeline_config: Config):
    for _name, pipeline in pipeline_config.pipelines.items():
        result = PipelineConverter(
            config=pipeline_config,
            commit_identifier="latest",
        ).convert_pipeline(pipeline)
        assert result["nodes"]
        assert result["edges"]


def test_pipeline_conversion_override_order(pipeline_config: Config):
    result = PipelineConverter(
        config=pipeline_config,
        commit_identifier="latest",
    ).convert_pipeline(pipeline_config.pipelines["My medium pipeline"])
    train_node = next(node for node in result["nodes"] if node["name"] == "train")
    # If conversion order is incorrect, this will have remained a list
    assert isinstance(train_node["template"]["inputs"], dict)


def test_pipeline_conversion_no_output_timeout(pipeline_config: Config):
    result = PipelineConverter(
        config=pipeline_config,
        commit_identifier="latest",
    ).convert_pipeline(pipeline_config.pipelines["My medium pipeline"])
    train_node = next(node for node in result["nodes"] if node["name"] == "train")
    assert (
        train_node["template"]["runtime_config"]["no_output_timeout"]
        == parse_duration_string("6h").total_seconds()
    )


def test_pipeline_conversion_override_inputs(pipeline_overridden_config: Config):
    result = PipelineConverter(
        config=pipeline_overridden_config,
        commit_identifier="latest",
    ).convert_pipeline(
        pipeline_overridden_config.pipelines["My overriden input pipeline"],
    )

    merged = next(node for node in result["nodes"] if node["name"] == "merged")
    assert merged["template"]["command"][0] == "merge date"
    assert merged["template"]["image"] == "merge node image"
    assert isinstance(merged["template"]["inputs"], dict)
    assert len(merged["template"]["inputs"].get("training-images", [])) == 2
    assert (
        merged["template"]["inputs"].get("training-images", [])[0]
        == "merged node image 1"
    )
    assert len(merged["template"]["parameters"].items()) == 3

    overridden = next(node for node in result["nodes"] if node["name"] == "overridden")
    assert isinstance(overridden["template"]["inputs"], dict)
    assert (
        overridden["template"]["inputs"].get("training-images", [])[0]
        == "overridden node image"
    )
    assert len(overridden["template"]["inputs"].get("training-images", [])) == 1
    assert len(overridden["template"]["parameters"].items()) == 3


def test_pipeline_parameter_conversion(pipeline_with_parameters_config):
    for _name, pipe in pipeline_with_parameters_config.pipelines.items():
        result = PipelineConverter(
            config=pipeline_with_parameters_config,
            commit_identifier="latest",
        ).convert_pipeline(pipe)
        for parameter_name in [param.name for param in pipe.parameters]:
            assert isinstance(result["parameters"], dict)
            assert result["parameters"][parameter_name]

            parameter = result["parameters"][parameter_name]
            assert parameter["config"]["targets"]
            assert "target" not in parameter["config"]
            assert isinstance(parameter["config"]["targets"], list)

            # When pipeline parameter has no default value, the expression should be empty
            parameter_config = next(
                param for param in pipe.parameters if param.name == parameter_name
            )
            expression_value = (
                parameter_config.default if parameter_config.default is not None else ""
            )
            assert parameter["expression"] == expression_value
            assert type(parameter["expression"]) == type(expression_value)
