from enum import Enum
from typing import List, Optional, Union

from valohai_yaml.lint import LintResult
from valohai_yaml.objs.base import Item
from valohai_yaml.objs.pipelines.node_action import NodeAction
from valohai_yaml.objs.utils import check_type_and_listify, consume_array_of
from valohai_yaml.types import LintContext, SerializedDict
from valohai_yaml.utils.lint import lint_iterables


class ErrorAction(Enum):
    """What should happen when error occurs in nodes execution."""

    STOP_ALL = "stop-all"  # default: stop whole pipeline on error
    STOP_NEXT = "stop-next"  # stop only following nodes on error
    CONTINUE = "continue"  # continue pipeline as error never occurred

    @classmethod
    def cast(cls, value: Optional[Union["ErrorAction", str]]) -> "ErrorAction":
        if not value:
            return ErrorAction.STOP_ALL
        if isinstance(value, ErrorAction):
            return value
        value = str(value).lower()
        if value == "none":
            return ErrorAction.STOP_ALL
        return ErrorAction(value)


class Node(Item):
    """Generic node base class."""

    # `type` must be set in subclasses
    type: str

    # `name` will be set on instance level in subclasses
    name: str

    # `actions` will be set on instance level in subclasses
    actions: List[NodeAction]

    # `on_error` what the pipeline should do when this node is erroneous: "stop-all" default, "continue"
    on_error: ErrorAction

    def __init__(
        self,
        *,
        name: str,
        actions: Optional[List[NodeAction]] = None,
        on_error: Union[str, ErrorAction] = ErrorAction.STOP_ALL,
    ) -> None:
        self.name = name
        self.actions = check_type_and_listify(
            actions,
            NodeAction,
            parse=NodeAction.parse,
        )
        self.on_error = ErrorAction.cast(on_error)

    @classmethod
    def parse_qualifying(cls, data: SerializedDict) -> "Node":
        node_type_map = {
            sc.type: sc for sc in cls.__subclasses__() if getattr(sc, "type", None)
        }
        data = data.copy()
        subcls = node_type_map[data.pop("type")]
        data["actions"] = consume_array_of(data, "actions", NodeAction)
        return subcls.parse(data)

    def serialize(self) -> SerializedDict:
        ser = dict(super().serialize())
        ser["type"] = self.type
        if not ser.get("actions"):
            ser.pop("actions", None)
        return ser

    def lint(self, lint_result: LintResult, context: LintContext) -> None:
        super().lint(lint_result, context)
        context = dict(context, node=self)
        lint_iterables(lint_result, context, (self.actions,))

    def get_data(self) -> SerializedDict:
        data = super().get_data()
        data["on_error"] = data["on_error"].value
        return data

    def __repr__(self) -> str:  # noqa: D105
        return f'<{self.type.title()} Node "{self.name}">'
