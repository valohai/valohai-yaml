from typing import List, Optional, Union

from valohai_yaml.lint import LintResult
from valohai_yaml.objs.pipelines.node import ErrorAction, Node
from valohai_yaml.objs.pipelines.node_action import NodeAction
from valohai_yaml.types import LintContext


class DeploymentNode(Node):
    """Represents a deployment node within a pipeline definition."""

    type = "deployment"

    def __init__(
        self,
        *,
        name: str,
        deployment: str,
        actions: Optional[List[NodeAction]] = None,
        endpoints: Optional[List[str]] = None,
        aliases: Optional[List[str]] = None,
        on_error: Union[str, ErrorAction] = ErrorAction.STOP_ALL,
    ) -> None:
        super().__init__(name=name, actions=actions, on_error=on_error)
        if aliases is None:
            aliases = []
        if endpoints is None:
            endpoints = []
        self.deployment = deployment
        self.endpoints = endpoints
        self.aliases = aliases

    def lint(self, lint_result: LintResult, context: LintContext) -> None:
        super().lint(lint_result, context)

        if not self.name:
            lint_result.add_error(
                "Deployment has no name",
            )
