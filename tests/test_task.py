from valohai_yaml.objs import Config, Task
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
