from typing import List, Optional

from ...lint import LintResult
from ...utils.lint import lint_iterables
from ..base import Item
from ..utils import check_type_and_listify, consume_array_of
from .node_action import NodeAction


class Node(Item):
    """Generic node base class."""

    # `type` must be set in subclasses
    type = None  # type: str

    # `name` will be set on instance level in subclasses
    # TODO: change to a type annotation when dropping py3.5
    name = None  # type: str

    # `actions` will be set on instance level in subclasses
    # TODO: change to a type annotation when dropping py3.5
    actions = None  # type: List[NodeAction]

    def __init__(
        self,
        *,
        name: str,
        actions: Optional[List[NodeAction]] = None
    ) -> None:
        self.name = name
        self.actions = check_type_and_listify(actions, NodeAction)

    @classmethod
    def parse_qualifying(cls, data: dict) -> 'Node':
        node_type_map = {
            sc.type: sc
            for sc in cls.__subclasses__()
            if getattr(sc, 'type', None)
        }
        data = data.copy()
        subcls = node_type_map[data.pop('type')]
        data['actions'] = consume_array_of(data, 'actions', NodeAction)
        return subcls.parse(data)

    def serialize(self) -> dict:
        ser = super().serialize()
        ser['type'] = self.type
        return ser

    def lint(self, lint_result: LintResult, context: dict) -> None:
        super().lint(lint_result, context)
        context = dict(context, node=self)
        lint_iterables(lint_result, context, (
            self.actions,
        ))

    def __repr__(self) -> str:  # noqa: D105
        return '<{type} Node "{name}">'.format(
            type=self.type.title(),
            name=self.name,
        )
