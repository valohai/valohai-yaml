from .node import Node
from ..base import Item


class Deployment(Item):
    def __init__(self, name, endpoints) -> None:
        self.name = name
        self.endpoints = endpoints


class DeploymentNode(Node):
    type = 'deployment'

    def __init__(
        self,
        *,
        name,
        deployment,
        endpoints
    ) -> None:
        self.name = name
        self.deployment = deployment
        self.endpoints = endpoints

    def lint(self, lint_result, context: dict) -> None:
        super().lint(lint_result, context)

        if not self.name:
            lint_result.add_error(
                'Deployment has no name'
            )

        if not self.endpoints:
            lint_result.add_error('Deployment {} has no endpoints'.format(self.name))
