from valohai_yaml.objs import Config, Task
from valohai_yaml.objs.task import TaskOnChildError, TaskType
from valohai_yaml.objs.variant_parameter import VariantParameterStyle


def test_tasks_parameters(task_config: Config):
    for name, task in task_config.tasks.items():
        assert isinstance(task, Task)
        assert task.name == name
        assert task.step in task_config.steps
        assert isinstance(task.parameters, list)
        if len(task.parameters) > 0:
            assert task.parameters[0].name == "A"
            assert isinstance(task.parameters[0].style, VariantParameterStyle)


def test_task_additional_fields_1(task_config: Config):
    task = task_config.tasks["task 4 logspace"]
    assert task.execution_batch_size == 42
    assert task.execution_count == 420
    assert task.maximum_queued_executions == 17
    assert task.on_child_error == TaskOnChildError.STOP_ALL_AND_ERROR
    assert task.type == TaskType.RANDOM_SEARCH


def test_task_additional_fields_2(task_config: Config):
    task = task_config.tasks["task 1 single"]
    assert task.type == TaskType.BAYESIAN_TPE
    assert task.optimization_target_metric == "goodness"
    assert task.optimization_target_value == 7.2


def test_task_parameter_sets(task_config: Config):
    task = task_config.tasks["parameter sets"]
    assert task.parameter_sets == [
        {"A": 5, "B": 6},
        {"A": 8, "B": 9},
        {"A": 72, "B": 42},
    ]
    assert task.type == TaskType.MANUAL_SEARCH
