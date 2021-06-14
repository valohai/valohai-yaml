from typing import Any, Dict, Iterable, Optional, Union

from .base import Item
from .file import File


class Endpoint(Item):
    """Represents a deployment endpoint."""

    def __init__(
        self,
        *,
        name: str,
        image: str,
        description: Optional[str] = None,
        files: Iterable[File] = (),
        port: Optional[Union[str, int]] = None,
        server_command: Optional[str] = None,
        wsgi: Optional[str] = None
    ) -> None:
        self.name = name
        self.description = description
        self.image = image
        self.port = port
        self.server_command = server_command
        self.wsgi = wsgi

        files = list(files)  # Listify iterators
        assert all(isinstance(f, File) for f in files)
        self.files = files

    @classmethod
    def parse(cls, kwargs: Dict[str, Any]) -> 'Endpoint':
        data = dict(
            kwargs,
            files=[File.parse(f) for f in kwargs.get('files', ())],
        )
        return super().parse(data)
