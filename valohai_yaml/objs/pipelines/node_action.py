from __future__ import annotations

from typing import TYPE_CHECKING

from valohai_yaml.objs.base import Item
from valohai_yaml.utils import listify

if TYPE_CHECKING:
    from collections.abc import Iterable

    from valohai_yaml.lint import LintResult
    from valohai_yaml.types import LintContext, SerializedDict

WELL_KNOWN_WHENS = {
    "node-complete",  # Node completed (successfully)
    "node-starting",  # Node about to start
    "node-error",  # Node errored
}

WELL_KNOWN_THENS = {
    "noop",  # For testing
    "stop-pipeline",
    "error-pipeline",
}


class NodeAction(Item):
    """Represents a node action."""

    def __init__(
        self,
        *,
        when: str | Iterable[str],
        if_: None | str | list[str],
        then: None | str | list[str],
    ) -> None:
        self.when: set[str] = {str(watom).lower() for watom in listify(when)}
        self.if_: list[str] = listify(if_)
        self.then: list[str] = listify(then)

    @classmethod
    def parse(cls, data: SerializedDict) -> NodeAction:
        data = data.copy()
        data["if_"] = data.pop("if", [])
        return super().parse(data)

    def get_data(self) -> SerializedDict:
        data = super().get_data()
        data["if"] = data.pop("if_")
        data["when"] = sorted(data.pop("when"))
        return data

    def lint(self, lint_result: LintResult, context: LintContext) -> None:
        super().lint(lint_result, context)
        for when in self.when:
            if when not in WELL_KNOWN_WHENS:
                lint_result.add_warning(
                    f'"when" value {self.when} is not well-known; the action might never be triggered',
                )
        for then in self.then:
            if then not in WELL_KNOWN_THENS:
                lint_result.add_warning(
                    f'"then" value {self.then} is not well-known; the action might do nothing',
                )
