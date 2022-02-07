from typing import List, Optional

from ...lint import LintResult
from ...types import LintContext, SerializedDict
from ...utils.lint import lint_iterables
from ..base import Item
from ..utils import check_type_and_listify, consume_array_of
from .node_action import NodeAction


class Node(Item):
    """Generic node base class."""

    # `type` must be set in subclasses
    type: str

    # `name` will be set on instance level in subclasses
    name: str

    # `actions` will be set on instance level in subclasses
    actions: List[NodeAction]

    # `continue_on_error` if pipeline execution should continue even when node was erroneous
    continue_on_error: bool

    def __init__(
        self,
        *,
        name: str,
        actions: Optional[List[NodeAction]] = None,
        continue_on_error: bool = False,
    ) -> None:
        self.name = name
        self.actions = check_type_and_listify(actions, NodeAction, parse=NodeAction.parse)
        self.continue_on_error = bool(continue_on_error)

    @classmethod
    def parse_qualifying(cls, data: SerializedDict) -> 'Node':
        node_type_map = {
            sc.type: sc
            for sc in cls.__subclasses__()
            if getattr(sc, 'type', None)
        }
        data = data.copy()
        subcls = node_type_map[data.pop('type')]
        data['actions'] = consume_array_of(data, 'actions', NodeAction)
        return subcls.parse(data)

    def serialize(self) -> SerializedDict:
        ser = dict(super().serialize())
        ser['type'] = self.type
        if not ser.get('actions'):
            ser.pop('actions', None)
        return ser

    def lint(self, lint_result: LintResult, context: LintContext) -> None:
        super().lint(lint_result, context)
        context = dict(context, node=self)
        lint_iterables(lint_result, context, (
            self.actions,
        ))

    def __repr__(self) -> str:  # noqa: D105
        return f'<{self.type.title()} Node "{self.name}">'
