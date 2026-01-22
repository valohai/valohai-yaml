from tests.utils import get_error_example_path
from valohai_yaml import parse
from valohai_yaml.lint import lint_file
from valohai_yaml.objs import Config
from valohai_yaml.objs.pipelines.task_node import TaskNode
from valohai_yaml.pipelines.conversion import PipelineConverter


def test_task_blueprint_reference_validates(task_blueprint_pipeline_config: Config):
    lint_result = task_blueprint_pipeline_config.lint()
    assert lint_result.is_valid()


def test_task_blueprint_serializes(task_blueprint_pipeline_config: Config):
    pipeline = task_blueprint_pipeline_config.pipelines["train-pipeline"]

    node = pipeline.get_node_by(name="train")
    assert isinstance(node, TaskNode)

    serialized = node.serialize()
    assert serialized["type"] == "task"
    assert serialized["task"] == "my-sweep"


def test_referenced_task_blueprint_is_missing():
    path = get_error_example_path("invalid-task-blueprint-reference.yaml")

    lint_result = lint_file(path)
    assert not lint_result.is_valid()

    errors = list(lint_result.errors)
    assert any("my-non-existent-task" in err["message"] and "does not exist" in err["message"] for err in errors)


def test_task_node_with_blueprint_converts_to_api_call(task_blueprint_pipeline_config: Config):
    pipeline = task_blueprint_pipeline_config.pipelines["train-pipeline"]
    payload = PipelineConverter(
        config=task_blueprint_pipeline_config,
        commit_identifier="abc123",
    ).convert_pipeline(pipeline)

    train_node = next(node for node in payload["nodes"] if node["name"] == "train")
    assert train_node["type"] == "task"
    assert train_node["template"]["commit"] == "abc123"

    # has the right underlying step
    assert train_node["template"]["step"] == "train-model"

    # task related properties come from the blueprint
    assert train_node["template"]["type"] == "grid_search"
    assert train_node["template"]["maximum_queued_executions"] == 2
    assert train_node["template"]["on_child_error"] == "stop-all-and-error"

    # parameters come from the blueprint, not the step
    assert train_node["template"]["parameters"]["epochs"] == {
        "style": "multiple",
        "rules": {"items": [30, 40, 50]},
    }


BLUEPRINT_TASK_NODE_WITH_OVERRIDE_YAML = """
- step:
    name: train-model
    image: python:3.12
    command:
      - echo "training"
    parameters:
      - name: epochs
        type: integer
        default: 10
      - name: learning_rate
        type: float
        default: 0.001
      - name: batch_size
        type: integer
        default: 32
    inputs:
      - name: dataset
        default: s3://bucket/step-default.csv
      - name: extra-data
        default: s3://bucket/step-extra.csv

- task:
    name: my-sweep
    step: train-model
    type: grid_search
    maximum-queued-executions: 5
    parameters:
      - name: learning_rate
        style: multiple
        rules:
          items: [0.01, 0.001]

- pipeline:
    name: train-pipeline
    nodes:
      - name: train
        type: task
        task: my-sweep
        override:
          parameters:
            - name: epochs
              default: 50
          inputs:
            - name: dataset
              default: s3://bucket/override.csv
    edges: []
"""


def test_blueprint_task_nodes_convert_with_step_overrides():
    config = parse(BLUEPRINT_TASK_NODE_WITH_OVERRIDE_YAML)
    pipeline = config.pipelines["train-pipeline"]
    payload = PipelineConverter(
        config=config,
        commit_identifier="abc123",
    ).convert_pipeline(pipeline)

    train_node = next(node for node in payload["nodes"] if node["name"] == "train")

    # task config comes from the blueprint
    assert train_node["template"]["type"] == "grid_search"
    assert train_node["template"]["maximum_queued_executions"] == 5

    # one parameter from node override (epochs)
    assert train_node["template"]["parameters"]["epochs"] == 50

    # one parameter from task blueprint, variant style (learning_rate)
    assert train_node["template"]["parameters"]["learning_rate"] == {
        "style": "multiple",
        "rules": {"items": [0.01, 0.001]},
    }

    # one parameter from step defaults (batch_size)
    assert train_node["template"]["parameters"]["batch_size"] == 32

    # one input from node override (dataset)
    assert train_node["template"]["inputs"]["dataset"] == ["s3://bucket/override.csv"]

    # one input from step defaults (extra-data)
    assert train_node["template"]["inputs"]["extra-data"] == ["s3://bucket/step-extra.csv"]


BLUEPRINT_WITH_ALL_FIELDS_YAML = """
- step:
    name: train-model
    image: python:3.12
    command: echo "training..."
    parameters:
      - name: learning_rate
        type: float
        default: 0.001

- task:
    name: bayesian-sweep
    step: train-model
    type: bayesian_tpe
    on-child-error: continue-and-complete
    maximum-queued-executions: 3
    execution-count: 100
    execution-batch-size: 10
    optimization-target-metric: val_loss
    optimization-target-value: 0.01
    engine: optuna
    stop-condition: execution.duration > 3600
    reuse-children: true
    parameters:
      - name: learning_rate
        style: multiple
        rules:
          items: [0.01, 0.001]

- pipeline:
    name: test-pipeline
    nodes:
      - name: bayesian-node
        type: task
        task: bayesian-sweep
    edges: []
"""


def test_blueprint_task_nodes_convert_with_all_fields():
    config = parse(BLUEPRINT_WITH_ALL_FIELDS_YAML)

    lint_result = config.lint()
    assert lint_result.is_valid()
    assert not list(lint_result.warnings)

    pipeline = config.pipelines["test-pipeline"]
    payload = PipelineConverter(
        config=config,
        commit_identifier="abc123",
    ).convert_pipeline(pipeline)

    node = next(node for node in payload["nodes"] if node["name"] == "bayesian-node")
    template = node["template"]

    assert template["type"] == "bayesian_tpe"
    assert template["on_child_error"] == "continue-and-complete"
    assert template["maximum_queued_executions"] == 3
    assert template["stop_expression"] == "execution.duration > 3600"
    assert template["allow_reuse"] is True
    assert template["configuration"]["execution_count"] == 100
    assert template["configuration"]["execution_batch_size"] == 10
    assert template["configuration"]["optimization_target_metric"] == "val_loss"
    assert template["configuration"]["optimization_target_value"] == 0.01
    assert template["configuration"]["engine"] == "optuna"
    assert template["parameters"] == {
        "learning_rate": {
            "style": "multiple",
            "rules": {"items": [0.01, 0.001]},
        },
    }


BLUEPRINT_WITH_MANY_PARAMETER_SETS = """
- step:
    name: train-model
    image: python:3.12
    command: echo "training..."
    parameters:
      - name: epochs
        type: integer
        default: 999
      - name: learning_rate
        type: float
        default: 0.1

- task:
    name: many-sweep
    step: train-model
    type: manual_search
    reuse-children: true
    parameter-sets:
      - epochs: 10
        learning_rate: 0.01
      - epochs: 20
        learning_rate: 0.001

- pipeline:
    name: test-pipeline
    nodes:
      - name: manual-node
        type: task
        task: many-sweep
    edges: []
"""


def test_blueprint_task_nodes_converts_parameter_sets():
    config = parse(BLUEPRINT_WITH_MANY_PARAMETER_SETS)

    lint_result = config.lint()
    assert lint_result.is_valid()
    assert not list(lint_result.warnings)

    pipeline = config.pipelines["test-pipeline"]
    payload = PipelineConverter(
        config=config,
        commit_identifier="abc123",
    ).convert_pipeline(pipeline)

    node = next(node for node in payload["nodes"] if node["name"] == "manual-node")
    template = node["template"]

    assert template["type"] == "manual_search"
    assert template["parameters"] == {
        "epochs": {
            "style": "multiple",
            "rules": {"items": [10, 20]},
        },
        "learning_rate": {
            "style": "multiple",
            "rules": {"items": [0.01, 0.001]},
        },
    }
    assert "parameter_sets" not in template
