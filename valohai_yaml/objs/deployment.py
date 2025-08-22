from typing import Optional

from valohai_yaml.objs.base import Item
from valohai_yaml.types import DeploymentDefaultsDict


class Deployment(Item):
    """Represents a deployment in a project under where deployment versions and endpoints are housed."""

    def __init__(
        self,
        *,
        name: str,
        defaults: Optional[DeploymentDefaultsDict] = None,
    ) -> None:
        self.name = name
        self.defaults = defaults
