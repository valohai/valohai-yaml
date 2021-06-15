from typing import Iterable, List, Set, Union

from ...utils import listify
from ..base import Item


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
        return data
