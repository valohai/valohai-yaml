from valohai_yaml.objs.pipelines.execution_node import ExecutionNode
from valohai_yaml.objs.pipelines.node import Node


class TaskNode(ExecutionNode, Node):
    """Represents a task node within a pipeline definition."""

    type = "task"
