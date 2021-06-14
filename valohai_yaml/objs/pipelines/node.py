from ..base import Item


class Node(Item):
    """Generic node base class."""

    # `type` must be set in subclasses
    type = None  # type: str

    # `name` will be set on instance level in subclasses
    # TODO: change to a type annotation when dropping py3.5
    name = None  # type: str

    @classmethod
    def parse_qualifying(cls, data: dict) -> 'Node':
        node_type_map = {
            sc.type: sc
            for sc in cls.__subclasses__()
            if getattr(sc, 'type', None)
        }
        data = data.copy()
        subcls = node_type_map[data.pop('type')]
        return subcls.parse(data)

    def serialize(self) -> dict:
        ser = super().serialize()
        ser['type'] = self.type
        return ser
