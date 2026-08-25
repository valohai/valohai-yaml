from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

from valohai_yaml.objs.base import Item
from valohai_yaml.objs.file import File
from valohai_yaml.objs.utils import check_type_and_listify

if TYPE_CHECKING:
    from collections.abc import Iterable

    from valohai_yaml.lint import LintResult
    from valohai_yaml.types import (
        EndpointResourcesDict,
        EndpointSharedVolumeDict,
        EndpointTolerationDict,
        LintContext,
        SerializedDict,
    )


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
        shared_volumes: list[EndpointSharedVolumeDict] | None = None,
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
        self.shared_volumes = shared_volumes

    @classmethod
    def parse(cls, data: SerializedDict) -> Endpoint:
        data = dict(
            data,
            files=[File.parse(f) for f in data.get("files", ())],
        )
        return super().parse(data)

    def lint(self, lint_result: LintResult, context: LintContext) -> None:
        super().lint(lint_result, context)

        shared_volumes = self.shared_volumes or []
        for shared_volume in shared_volumes:
            mount_path = shared_volume.get("mount-path", "")
            if not mount_path.startswith("/"):
                lint_result.add_error(
                    f'Endpoint "{self.name}" shared volume mount path "{mount_path}" must start with "/"',
                )
            sub_path = shared_volume.get("sub-path", "")
            if sub_path.startswith("/"):
                lint_result.add_error(
                    f'Endpoint "{self.name}" shared volume sub-path "{sub_path}" must not start with "/"',
                )

        mount_path_counts = Counter(shared_volume.get("mount-path") for shared_volume in shared_volumes)
        for mount_path, times in mount_path_counts.items():
            if times > 1:
                lint_result.add_error(
                    f'Endpoint "{self.name}" has {times} shared volumes mounted at "{mount_path}"',
                )
