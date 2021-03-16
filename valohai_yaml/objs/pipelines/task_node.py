from .node import Node
from .execution_node import ExecutionNode


class TaskNode(ExecutionNode, Node):
    type = 'task'
