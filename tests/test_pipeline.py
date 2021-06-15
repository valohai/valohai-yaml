from valohai_yaml.objs import Config, DeploymentNode


def test_pipeline_valid(pipeline_config: Config):
    assert pipeline_config.lint().is_valid()


def test_little_pipeline(pipeline_config: Config):
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


def test_deployment_pipeline(pipeline_config: Config):
    dp = pipeline_config.pipelines["My deployment pipeline"]
    assert any(
        (
            edge.source_node == "train"
            and edge.source_type == "output"
            and edge.source_key == "model"
            and edge.target_node == "deploy-predictor"
            and edge.target_type == "file"
            and edge.target_key == "predict-digit.model"
        )
        for edge in dp.edges
    )

    dn_predict = dp.get_node_by(name='deploy-predictor')
    assert isinstance(dn_predict, DeploymentNode)
    assert "predictor-staging" in dn_predict.aliases
    assert "predict-digit" in dn_predict.endpoints

    dn_no_preset = dp.get_node_by(name='deploy-no-presets')
    assert isinstance(dn_no_preset, DeploymentNode)
    assert dn_no_preset.aliases == []
    assert dn_no_preset.endpoints == []


def test_medium_pipeline(pipeline_config: Config):
    assert any(
        (edge.source_type == "output" and edge.source_key == "model.pb")
        for edge in pipeline_config.pipelines["My medium pipeline"].edges
    )
