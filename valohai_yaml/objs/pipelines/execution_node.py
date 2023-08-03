from typing import Any, Dict, List, Optional, Union

from valohai_yaml.lint import LintResult
from valohai_yaml.objs.pipelines.node import ErrorAction, Node
from valohai_yaml.objs.pipelines.node_action import NodeAction
from valohai_yaml.objs.pipelines.override import Override
from valohai_yaml.types import LintContext, NodeOverrideDict


class ExecutionNode(Node):
    """Represents an execution node within a pipeline definition."""

    type = 'execution'
    override: Optional[Override]

    def __init__(
        self,
        *,
        name: str,
        step: str,
        actions: Optional[List[NodeAction]] = None,
        override: Optional[Union[Override, NodeOverrideDict]] = None,
        on_error: Union[str, ErrorAction] = ErrorAction.STOP_ALL,
    ) -> None:
        super().__init__(name=name, actions=actions, on_error=on_error)
        self.step = step
        if override is None or isinstance(override, Override):
            self.override = override
        else:
            self.override = Override.parse(override)

    def lint(self, lint_result: LintResult, context: LintContext) -> None:
        super().lint(lint_result, context)
        config = context['config']
        pipeline = context['pipeline']
        if self.step not in config.steps:
            lint_result.add_error(f'Pipeline {pipeline.name} node {self.name} step {self.step} does not exist')

    def get_parameter_defaults(self) -> Dict[str, Any]:
        if not self.override or self.override.parameters is None:
            return {}
        return {
            name: parameter.default
            for (name, parameter)
            in self.override.parameters.items()
            if parameter.default is not None
        }
