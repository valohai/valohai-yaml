from typing import List, Optional, TYPE_CHECKING, Union

from valohai_yaml.excs import ValidationError
from valohai_yaml.lint import LintResult

if TYPE_CHECKING:
    from valohai_yaml.objs import Pipeline

from ..base import Item


def _split_prop(prop: str) -> List[str]:
    return prop.split('.', 2)


edge_types = {'input', 'output', 'parameter', 'metadata', 'file'}


class Edge(Item):
    """Represents an edge within a pipeline definition."""

    def __init__(
        self,
        *,
        source: str,
        target: str,
        configuration: Optional[dict] = None
    ) -> None:
        if configuration is None:
            configuration = {}
        self.source = source
        self.target = target
        self.configuration = configuration

    @property
    def source(self) -> str:
        return '.'.join((self.source_node, self.source_type, self.source_key))

    @source.setter
    def source(self, prop: str) -> None:
        split = _split_prop(prop)
        if len(split) != 3:
            raise ValidationError(f"Source specifier {prop!r} must have 3 parts (it has {len(split)})")
        self.source_node, self.source_type, self.source_key = split

    @property
    def target(self) -> str:
        return '.'.join((self.target_node, self.target_type, self.target_key))

    @target.setter
    def target(self, prop: str) -> None:
        split = _split_prop(prop)
        if len(split) != 3:
            raise ValidationError(f"Target specifier {prop!r} must have 3 parts (it has {len(split)})")
        self.target_node, self.target_type, self.target_key = split

    @classmethod
    def parse(cls, data: Union[dict, list]) -> 'Edge':
        if isinstance(data, list):  # Must be a shorthand
            if len(data) != 2:
                raise ValidationError(f'Malformed edge shorthand {data}')
            data = {'source': data[0], 'target': data[1]}
        return super().parse(data)

    def get_data(self) -> dict:
        return {
            'source': self.source,
            'target': self.target,
            'configuration': self.configuration,
        }

    def lint(self, lint_result: LintResult, context: dict) -> None:
        pipeline = context['pipeline']  # type: Pipeline
        node_map = pipeline.node_map
        if self.source_node not in node_map:
            lint_result.add_error(
                f'Pipeline {pipeline.name} edge source node {self.source_node} does not exist'
            )
        if self.target_node not in node_map:
            lint_result.add_error(
                f'Pipeline {pipeline.name} edge target node {self.target_node} does not exist'
            )
        if self.source_type not in edge_types:
            lint_result.add_error(
                f'Pipeline {pipeline.name} source type {self.source_type} '
                f'(between {self.source_node} and {self.target_node}) not valid'
            )
        if self.target_type not in edge_types:
            lint_result.add_error(
                f'Pipeline {pipeline.name} target type {self.target_type} '
                f'(between {self.source_node} and {self.target_node}) not valid'
            )
