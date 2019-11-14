from ..base import Item


class Node(Item):
    type = None  # must be set in subclasses

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
