from ...lint import LintResult
from .node import Node


class ExecutionNode(Node):
    """Represents an execution node within a pipeline definition."""

    type = 'execution'

    def __init__(
        self,
        *,
        name: str,
        step: str,
        override: dict = None
    ) -> None:
        if override is None:
            override = {}
        self.name = name
        self.step = step
        self.override = override

    def lint(self, lint_result: LintResult, context: dict) -> None:
        super().lint(lint_result, context)
        config = context['config']
        pipeline = context['pipeline']
        if self.step not in config.steps:
            lint_result.add_error('Pipeline {pipeline} node {node} step {step} does not exist'.format(
                pipeline=pipeline.name,
                node=self.name,
                step=self.step,
            ))
