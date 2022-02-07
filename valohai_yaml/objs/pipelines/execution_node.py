from typing import List, Optional

from ...lint import LintResult
from ...types import LintContext, NodeOverrideDict
from .node import Node
from .node_action import NodeAction


class ExecutionNode(Node):
    """Represents an execution node within a pipeline definition."""

    type = 'execution'

    def __init__(
        self,
        *,
        name: str,
        step: str,
        actions: Optional[List[NodeAction]] = None,
        override: Optional[NodeOverrideDict] = None,
        continue_on_error: bool = False,
    ) -> None:
        super().__init__(name=name, actions=actions, continue_on_error=continue_on_error)
        if override is None:
            override = {}
        self.step = step
        self.override = override

    def lint(self, lint_result: LintResult, context: LintContext) -> None:
        super().lint(lint_result, context)
        config = context['config']
        pipeline = context['pipeline']
        if self.step not in config.steps:
            lint_result.add_error(f'Pipeline {pipeline.name} node {self.name} step {self.step} does not exist')
