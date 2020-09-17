from valohai_yaml.objs import Config


def test_pipeline(pipeline_config: Config):
    lr = pipeline_config.lint()
    assert lr.is_valid()
    assert any(
        (
            edge.source_node == "batch1"
            and edge.source_type == "parameter"
            and edge.source_key == "aspect-ratio"
            and edge.target_node == "batch2"
            and edge.target_type == "parameter"
            and edge.target_key == "aspect-ratio"
        )
        for edge in pipeline_config.pipelines["My little pipeline"].edges
    )
    assert any(
        (
            edge.source_node == "train"
            and edge.source_type == "output"
            and edge.source_key == "model"
            and edge.target_node == "deploy"
            and edge.target_type == "file"
            and edge.target_key == "predict-digit.model"
        )
        for edge in pipeline_config.pipelines["My deployment pipeline"].edges
    )
    assert any(
        (edge.source_type == "output" and edge.source_key == "model.pb")
        for edge in pipeline_config.pipelines["My medium pipeline"].edges
    )
