from tests.utils import get_warning_example_path
from valohai_yaml.lint import lint_file
from valohai_yaml.objs import Config, DeploymentNode, ExecutionNode


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

    dn_predict = dp.get_node_by(name="deploy-predictor")
    assert isinstance(dn_predict, DeploymentNode)
    assert "predictor-staging" in dn_predict.aliases
    assert "predict-digit" in dn_predict.endpoints

    dn_no_preset = dp.get_node_by(name="deploy-no-presets")
    assert isinstance(dn_no_preset, DeploymentNode)
    assert dn_no_preset.aliases == []
    assert dn_no_preset.endpoints == []


def test_medium_pipeline(pipeline_config: Config):
    assert any(
        (edge.source_type == "output" and edge.source_key == "model.pb")
        for edge in pipeline_config.pipelines["My medium pipeline"].edges
    )


def test_action_pipeline(pipeline_config: Config):
    pl = pipeline_config.pipelines["Last action pipeline"]
    train_node = pl.get_node_by(name="train")
    assert train_node
    assert train_node.actions[0].get_data() == {
        "if": ["metadata.accuracy < .8"],
        "then": ["stop-pipeline"],
        "when": ["node-complete"],
    }
    validate_node = pl.get_node_by(name="validate")
    assert validate_node
    assert validate_node.actions[0].get_data() == {
        "if": [],
        "then": ["noop", "noop", "noop"],
        "when": ["node-complete"],
    }
    assert validate_node.actions[1].get_data() == {
        "if": ["a", "b", "c"],
        "then": ["noop"],
        "when": ["node-complete", "node-starting"],
    }
    error_node = pl.get_node_by(name="accuracy-error")
    assert error_node
    assert error_node.actions[0].get_data() == {
        "if": ["metadata.accuracy <= .8"],
        "then": ["error-pipeline"],
        "when": ["node-complete"],
    }


def test_empty_actions_not_serialized(pipeline_config: Config):
    pl = pipeline_config.pipelines["Last action pipeline"]
    train_node = pl.get_node_by(name="train")
    assert train_node
    train_node.actions.clear()
    assert "actions" not in train_node.serialize()


def test_empty_override_not_serialized(pipeline_config: Config):
    pl = pipeline_config.pipelines["My medium pipeline"]
    train_node = pl.get_node_by(name="train")
    assert isinstance(train_node, ExecutionNode)
    assert train_node and train_node.override
    train_node.override = None
    assert "override" not in train_node.serialize()


def test_invalid_override_is_parsed_but_warns():
    path = get_warning_example_path("override-with-extra-fields-warning.yaml")
    items = lint_file(path, validate_schema=False)
    assert items.warning_count == 1
    assert next(items.warnings)["message"].startswith("Unknown field")
