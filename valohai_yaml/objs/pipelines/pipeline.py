from collections import OrderedDict
from typing import Any, List, Optional

from valohai_yaml.lint import LintResult
from valohai_yaml.utils.lint import lint_iterables

from ..base import Item
from .edge import Edge
from .node import Node


class Pipeline(Item):
    """Represents a definition of a pipeline, containing nodes and edges."""

    def __init__(
        self,
        *,
        name: str,
        nodes: List[Node],
        edges: List[Edge]
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
        return super().parse(data)

    def lint(self, lint_result: LintResult, context: dict) -> None:
        context = dict(context, pipeline=self)
        lint_iterables(lint_result, context, (self.nodes, self.edges))

    def get_node_by(self, **kwargs: Any) -> Optional[Node]:
        """Get the first node that matches all the passed named arguments."""
        if not kwargs:
            return None
        for node in self.nodes:
            data = node.serialize()
            if all(item in data.items() for item in kwargs.items()):
                return node
        return None
