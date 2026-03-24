from __future__ import annotations

from typing import TYPE_CHECKING

from valohai_yaml.objs.base import Item
from valohai_yaml.objs.file import File
from valohai_yaml.objs.utils import check_type_and_listify

if TYPE_CHECKING:
    from collections.abc import Iterable

    from valohai_yaml.types import EndpointResourcesDict, EndpointTolerationDict, SerializedDict


class Endpoint(Item):
    """Represents a deployment endpoint."""

    def __init__(
        self,
        *,
        name: str,
        image: str,
        description: str | None = None,
        files: Iterable[File] = (),
        port: str | int | None = None,
        server_command: str | None = None,
        wsgi: str | None = None,
        node_selector: str | None = None,
        resources: EndpointResourcesDict | None = None,
        tolerations: list[EndpointTolerationDict] | None = None,
    ) -> None:
        self.name = name
        self.description = description
        self.image = image
        self.port = port
        self.server_command = server_command
        self.wsgi = wsgi
        self.files = check_type_and_listify(files, File)
        self.node_selector = node_selector
        self.resources = resources
        self.tolerations = tolerations

    @classmethod
    def parse(cls, data: SerializedDict) -> Endpoint:
        data = dict(
            data,
            files=[File.parse(f) for f in data.get("files", ())],
        )
        return super().parse(data)
