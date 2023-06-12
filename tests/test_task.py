from valohai_yaml.objs import Config, Task
from valohai_yaml.objs.variant_parameter import VariantParameterStyle


def test_tasks_parameters(step_with_tasks: Config):
    steps = step_with_tasks.steps
    tasks = step_with_tasks.tasks
    for task in tasks:
        assert isinstance(tasks[task], Task)
        assert tasks[task].name == task
        assert tasks[task].step in steps
        assert isinstance(tasks[task].parameters, list)
        if len(tasks[task].parameters) > 0:
            assert tasks[task].parameters[0].name == 'A'
            assert isinstance(tasks[task].parameters[0].style, VariantParameterStyle)
