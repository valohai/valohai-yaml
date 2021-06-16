from typing import Iterable, List, Set, Union

from ...lint import LintResult
from ...utils import listify
from ..base import Item

WELL_KNOWN_WHENS = {
    'node-complete',  # Node completed (successfully)
    'node-starting',  # Node about to start
    'node-error',  # Node errored
}

WELL_KNOWN_THENS = {
    'noop',  # For testing
    'stop-pipeline',
}


class NodeAction(Item):
    """Represents a node action."""

    def __init__(
        self,
        *,
        when: Union[str, Iterable[str]],
        if_: Union[None, str, List[str]],
        then: Union[None, str, List[str]]
    ) -> None:
        self.when = {str(watom).lower() for watom in listify(when)}  # type: Set[str]
        self.if_ = listify(if_)  # type: List[str]
        self.then = listify(then)  # type: List[str]

    @classmethod
    def parse(cls, data: dict) -> 'NodeAction':
        data = data.copy()
        data['if_'] = data.pop('if', [])
        return super().parse(data)

    def get_data(self) -> dict:
        data = super().get_data()
        data['if'] = data.pop('if_')
        data['when'] = sorted(data.pop('when'))
        return data

    def lint(self, lint_result: LintResult, context: dict) -> None:
        super().lint(lint_result, context)
        for when in self.when:
            if when not in WELL_KNOWN_WHENS:
                lint_result.add_warning(
                    '"when" value {when} is not well-known; the action might never be triggered'.format(when=self.when)
                )
        for then in self.then:
            if then not in WELL_KNOWN_THENS:
                lint_result.add_warning(
                    '"then" value {then} is not well-known; the action might do nothing'.format(then=self.then)
                )
