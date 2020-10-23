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
            and edge.target_node == "deploy-predictor"
            and edge.target_type == "file"
            and edge.target_key == "predict-digit.model"
        )
        for edge in pipeline_config.pipelines["My deployment pipeline"].edges
    )
    dp = pipeline_config.pipelines["My deployment pipeline"]

    dn_predict = [node for node in dp.nodes if node.type == 'deployment' and node.name == 'deploy-predictor'][0]
    assert "predictor-staging" in dn_predict.aliases
    assert "predict-digit" in dn_predict.endpoints

    dn_no_preset = [node for node in dp.nodes if node.type == 'deployment' and node.name == 'deploy-no-presets'][0]
    assert dn_no_preset.aliases == []
    assert dn_no_preset.endpoints == []

    assert any(
        (edge.source_type == "output" and edge.source_key == "model.pb")
        for edge in pipeline_config.pipelines["My medium pipeline"].edges
    )
