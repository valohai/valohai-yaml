from .execution_node import ExecutionNode
from .node import Node


class TaskNode(ExecutionNode, Node):
    """Represents a task node within a pipeline definition."""

    type = 'task'
