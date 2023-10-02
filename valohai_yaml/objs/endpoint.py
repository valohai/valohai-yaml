from typing import Iterable, Optional, Union

from valohai_yaml.objs.base import Item
from valohai_yaml.objs.file import File
from valohai_yaml.objs.utils import check_type_and_listify
from valohai_yaml.types import EndpointResourcesDict, SerializedDict


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
        wsgi: Optional[str] = None,
        node_selector: Optional[str] = None,
        resources: Optional[EndpointResourcesDict] = None,
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

    @classmethod
    def parse(cls, data: SerializedDict) -> "Endpoint":
        data = dict(
            data,
            files=[File.parse(f) for f in data.get("files", ())],
        )
        return super().parse(data)
