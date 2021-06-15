from typing import List, Optional

from valohai_yaml.lint import LintResult

from .node import Node
from .node_action import NodeAction


class DeploymentNode(Node):
    """Represents a deployment node within a pipeline definition."""

    type = 'deployment'

    def __init__(
        self,
        *,
        name: str,
        deployment: str,
        actions: Optional[List[NodeAction]] = None,
        endpoints: List[str] = None,
        aliases: List[str] = None
    ) -> None:
        super().__init__(name=name, actions=actions)
        if aliases is None:
            aliases = []
        if endpoints is None:
            endpoints = []
        self.deployment = deployment
        self.endpoints = endpoints
        self.aliases = aliases

    def lint(self, lint_result: LintResult, context: dict) -> None:
        super().lint(lint_result, context)

        if not self.name:
            lint_result.add_error(
                'Deployment has no name'
            )
