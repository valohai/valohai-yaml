from enum import Enum
from typing import Any, Dict, List, Optional, Union

from valohai_yaml.lint import LintResult
from valohai_yaml.objs.pipelines.node import ErrorAction, Node
from valohai_yaml.objs.pipelines.node_action import NodeAction
from valohai_yaml.types import LintContext, NodeOverrideDict, SerializedDict


class Mode(Enum):
    """What should happen when error occurs in nodes execution."""

    MERGE = 'merge'  # merge inputs in a node with inputs from step
    OVERRIDE = 'override'  # default: override inputs in a node

    @classmethod
    def cast(cls, value: Optional[Union['Mode', str]]) -> 'Mode':
        if not value:
            return Mode.OVERRIDE
        if isinstance(value, Mode):
            return value
        value = str(value).lower()
        return Mode(value)


class ExecutionNode(Node):
    """Represents an execution node within a pipeline definition."""

    type = 'execution'
    mode: Mode

    def __init__(
            self,
            *,
            name: str,
            step: str,
            actions: Optional[List[NodeAction]] = None,
            override: Optional[NodeOverrideDict] = None,
            on_error: Union[str, ErrorAction] = ErrorAction.STOP_ALL,

            mode: Union[str, Mode] = Mode.OVERRIDE
    ) -> None:
        super().__init__(name=name, actions=actions, on_error=on_error)
        if override is None:
            override = {}
        self.step = step
        self.override = override
        self.mode = Mode.cast(mode)

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
        data['mode'] = data['mode'].value
        return data

    def serialize(self) -> SerializedDict:
        ser = dict(super().serialize())
        ser['mode'] = self.mode.value
        if self.mode == Mode.OVERRIDE:
            ser.pop('mode', None)
        return ser
