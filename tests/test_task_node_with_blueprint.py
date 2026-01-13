from tests.utils import get_error_example_path
from valohai_yaml.lint import lint_file
from valohai_yaml.objs import Config
from valohai_yaml.objs.pipelines.task_node import TaskNode


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
