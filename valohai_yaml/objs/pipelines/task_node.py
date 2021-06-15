from .execution_node import ExecutionNode
from .node import Node


class TaskNode(ExecutionNode, Node):
    type = 'task'
