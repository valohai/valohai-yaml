from .node import Node


class DeploymentNode(Node):
    type = 'deployment'

    def __init__(
        self,
        *,
        name,
        deployment,
        endpoints=[],
        aliases=[]
    ) -> None:
        self.name = name
        self.deployment = deployment
        self.endpoints = endpoints
        self.aliases = aliases

    def lint(self, lint_result, context: dict) -> None:
        super().lint(lint_result, context)

        if not self.name:
            lint_result.add_error(
                'Deployment has no name'
            )
