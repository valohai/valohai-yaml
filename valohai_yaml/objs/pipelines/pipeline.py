from collections import Counter, OrderedDict
from typing import Any, List, Optional

from valohai_yaml.lint import LintResult
from valohai_yaml.objs.base import Item
from valohai_yaml.objs.pipelines.edge import Edge
from valohai_yaml.objs.pipelines.node import Node
from valohai_yaml.objs.pipelines.pipeline_parameter import PipelineParameter
from valohai_yaml.types import LintContext, SerializedDict
from valohai_yaml.utils.lint import lint_iterables


class Pipeline(Item):
    """Represents a definition of a pipeline, containing nodes and edges."""

    def __init__(
        self,
        *,
        name: str,
        nodes: List[Node],
        edges: List[Edge],
        parameters: Optional[List[PipelineParameter]] = None,
    ) -> None:
        self.name = name
        self.nodes = nodes
        self.edges = edges
        self.parameters = parameters or []

    @property
    def node_map(self) -> OrderedDict:  # type: ignore[type-arg]
        return OrderedDict((node.name, node) for node in self.nodes)

    @classmethod
    def parse(cls, data: SerializedDict) -> "Pipeline":
        data = data.copy()
        data["edges"] = [Edge.parse(e) for e in data.pop("edges", ())]
        data["nodes"] = [Node.parse_qualifying(n) for n in data.pop("nodes", ())]
        data["parameters"] = [
            PipelineParameter.parse(e) for e in data.pop("parameters", ())
        ]
        return super().parse(data)

    def get_data(self) -> SerializedDict:
        data = super().get_data()
        if not data.get("parameters"):
            del data["parameters"]
        return data

    def lint(self, lint_result: LintResult, context: LintContext) -> None:
        # ensure unique names for nodes
        node_name_counts = Counter(node.name for node in self.nodes)
        for name, times in node_name_counts.items():
            if times > 1:
                lint_result.add_error(
                    f"Pipeline {self.name} has {times} nodes with the same name of {name}",
                )

        # lint each node, edge and parameter
        context = dict(context, pipeline=self)
        lint_iterables(lint_result, context, (self.nodes, self.edges, self.parameters))

    def get_node_by(self, **kwargs: Any) -> Optional[Node]:
        """Get the first node that matches all the passed named arguments."""
        if not kwargs:
            return None
        for node in self.nodes:
            data = node.serialize()
            if all(item in data.items() for item in kwargs.items()):
                return node
        return None
