from collections import OrderedDict

from ...utils.lint import lint_iterables
from ..base import Item
from .edge import Edge
from .node import Node


class Pipeline(Item):

    def __init__(
        self,
        *,
        name,
        nodes,
        edges
    ) -> None:
        self.name = name
        self.nodes = nodes
        self.edges = edges

    @property
    def node_map(self) -> OrderedDict:
        return OrderedDict((node.name, node) for node in self.nodes)

    @classmethod
    def parse(cls, data: dict) -> 'Pipeline':
        data = data.copy()
        data['edges'] = [Edge.parse(e) for e in data.pop('edges', ())]
        data['nodes'] = [Node.parse_qualifying(n) for n in data.pop('nodes', ())]
        return super(Pipeline, cls).parse(data)

    def lint(self, lint_result, context: dict) -> None:
        context = dict(context, pipeline=self)
        lint_iterables(lint_result, context, (self.nodes, self.edges))
