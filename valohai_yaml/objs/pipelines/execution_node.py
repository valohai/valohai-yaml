from .node import Node


class ExecutionNode(Node):
    type = 'execution'

    def __init__(self, name, step, override=None):
        if override is None:
            override = {}
        self.name = name
        self.step = step
        self.override = override
