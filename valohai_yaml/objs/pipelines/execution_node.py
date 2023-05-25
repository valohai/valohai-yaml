
from typing import Any, Dict, List, Optional, Union

from valohai_yaml.lint import LintResult
from valohai_yaml.objs.enums import ErrorAction, OverrideMode
from valohai_yaml.objs.pipelines.node import Node
from valohai_yaml.objs.pipelines.node_action import NodeAction
from valohai_yaml.types import LintContext, NodeOverrideDict, SerializedDict


class ExecutionNode(Node):
    """Represents an execution node within a pipeline definition."""

    type = 'execution'
    override_mode: OverrideMode

    def __init__(
            self,
            *,
            name: str,
            step: str,
            actions: Optional[List[NodeAction]] = None,
            override: Optional[NodeOverrideDict] = None,
            on_error: Union[str, ErrorAction] = ErrorAction.STOP_ALL,
            override_mode: Union[str, OverrideMode] = OverrideMode.OVERRIDE
    ) -> None:
        super().__init__(name=name, actions=actions, on_error=on_error)
        if override is None:
            override = {}
        self.step = step
        self.override = override
        self.override_mode = OverrideMode.cast(override_mode)

    def lint(self, lint_result: LintResult, context: LintContext) -> None:
        super().lint(lint_result, context)
        config = context['config']
        pipeline = context['pipeline']
        if self.step not in config.steps:
            lint_result.add_error(f'Pipeline {pipeline.name} node {self.name} step {self.step} does not exist')

    def get_parameter_defaults(self) -> Dict[str, Any]:
        if "parameters" not in self.override:
            return {}
        return {
            param['name']: param['default']
            for param
            in self.override['parameters']
            if 'default' in param
        }
    def get_data(self) -> SerializedDict:
        data = super().get_data()
        data['override_mode'] = data['override_mode'].value
        return data
