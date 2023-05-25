from valohai_yaml.objs import Config
from valohai_yaml.pipelines.conversion import PipelineConverter


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


def test_pipeline_conversion_override_inputs(pipeline_overriden_config: Config):
    result = PipelineConverter(
        config=pipeline_overriden_config,
        commit_identifier="latest",
    ).convert_pipeline(pipeline_overriden_config.pipelines["My overriden input pipeline"])
    merged = next(node for node in result["nodes"] if node["name"] == "merged")
    overridden = next(node for node in result["nodes"] if node["name"] == "overridden")
    # If conversion order is incorrect, this will have remained a list
    assert isinstance(merged["template"]["inputs"], dict)
    assert len(merged["template"]["inputs"].get('training-images', [])) == 2
    assert isinstance(overridden["template"]["inputs"], dict)
    assert len(overridden["template"]["inputs"].get('training-images', [])) == 1
