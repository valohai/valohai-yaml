from typing import Dict, Union, Optional, Any

from .base import Item


class Mount(Item):
    def __init__(
        self,
        *,
        source,
        destination,
        readonly=False,
        type: Optional[str] = None,
        options: Optional[dict] = None
    ) -> None:
        if options is None:
            options = {}
        self.source = source
        self.destination = destination
        self.readonly = bool(readonly)
        self.type = (str(type).lower() if type else None)
        self.options = options

    @classmethod
    def parse(cls, data: Union[Dict[str, Any], str]) -> 'Mount':
        if isinstance(data, str):
            source, destination = str(data).split(':', 1)
            data = {
                'source': source,
                'destination': destination,
            }
        return super().parse(data)

    def get_data(self) -> dict:
        data = super().get_data()
        if self.options:
            data['options'] = {str(k): v for (k, v) in self.options.items() if v is not None}
        else:
            data.pop('options', None)
        return data
