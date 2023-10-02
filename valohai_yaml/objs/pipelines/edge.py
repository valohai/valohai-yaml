from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from valohai_yaml.excs import ValidationError
from valohai_yaml.lint import LintResult
from valohai_yaml.types import EdgeConfigurationDict, LintContext, SerializedDict
from valohai_yaml.utils.node_socket_utils import split_socket_str

if TYPE_CHECKING:
    from valohai_yaml.objs import Pipeline

from valohai_yaml.objs.base import Item

edge_types = {"input", "output", "parameter", "metadata", "file"}


class Edge(Item):
    """Represents an edge within a pipeline definition."""

    def __init__(
        self,
        *,
        source: str,
        target: str,
        configuration: Optional[EdgeConfigurationDict] = None,
    ) -> None:
        if configuration is None:
            configuration = {}
        self.source = source
        self.target = target
        self.configuration = configuration

    @property
    def source(self) -> str:
        return ".".join((self.source_node, self.source_type, self.source_key))

    @source.setter
    def source(self, prop: str) -> None:
        split = split_socket_str(prop)
        if len(split) != 3:
            raise ValidationError(
                f"Source specifier {prop!r} must have 3 parts (it has {len(split)})",
            )
        self.source_node, self.source_type, self.source_key = split

    @property
    def target(self) -> str:
        return ".".join((self.target_node, self.target_type, self.target_key))

    @target.setter
    def target(self, prop: str) -> None:
        split = split_socket_str(prop)
        if len(split) != 3:
            raise ValidationError(
                f"Target specifier {prop!r} must have 3 parts (it has {len(split)})",
            )
        self.target_node, self.target_type, self.target_key = split

    @classmethod
    def parse(cls, data: Union[SerializedDict, List[Any]]) -> "Edge":
        if isinstance(data, list):  # Must be a shorthand
            if len(data) != 2:
                raise ValidationError(f"Malformed edge shorthand {data}")
            data = {"source": data[0], "target": data[1]}
        return super().parse(data)

    def get_data(self) -> SerializedDict:
        return {
            "source": self.source,
            "target": self.target,
            "configuration": self.configuration,
        }

    def get_expanded(self) -> Dict[str, Any]:
        """Get the "expanded" form of this edge."""
        result: Dict[str, Any] = {
            "source_node": self.source_node,
            "source_type": self.source_type,
            "source_key": self.source_key,
            "target_node": self.target_node,
            "target_type": self.target_type,
            "target_key": self.target_key,
        }
        if self.configuration:
            result["configuration"] = self.configuration
        return result

    def lint(self, lint_result: LintResult, context: LintContext) -> None:
        pipeline: Pipeline = context["pipeline"]
        node_map = pipeline.node_map
        if self.source_node not in node_map:
            lint_result.add_error(
                f"Pipeline {pipeline.name} edge source node {self.source_node} does not exist",
            )
        if self.target_node not in node_map:
            lint_result.add_error(
                f"Pipeline {pipeline.name} edge target node {self.target_node} does not exist",
            )
        if self.source_type not in edge_types:
            lint_result.add_error(
                f"Pipeline {pipeline.name} source type {self.source_type} "
                f"(between {self.source_node} and {self.target_node}) not valid",
            )
        if self.target_type not in edge_types:
            lint_result.add_error(
                f"Pipeline {pipeline.name} target type {self.target_type} "
                f"(between {self.source_node} and {self.target_node}) not valid",
            )
