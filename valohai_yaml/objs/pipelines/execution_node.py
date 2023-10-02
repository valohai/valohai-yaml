from typing import Any, Dict, List, Optional, Union

from valohai_yaml.lint import LintResult
from valohai_yaml.objs.pipelines.node import ErrorAction, Node
from valohai_yaml.objs.pipelines.node_action import NodeAction
from valohai_yaml.objs.pipelines.override import Override
from valohai_yaml.types import LintContext, NodeOverrideDict, SerializedDict


class ExecutionNode(Node):
    """Represents an execution node within a pipeline definition."""

    type = "execution"
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
        config = context["config"]
        pipeline = context["pipeline"]
        step = config.steps.get(self.step)
        error_prefix = f"Pipeline {pipeline.name} node {self.name} step {self.step}"
        if not step:
            lint_result.add_error(f"{error_prefix} does not exist")
            return
        if self.override is not None:
            self.override.lint(lint_result, context)
            step_inputs = step.inputs.keys()
            step_parameters = step.parameters.keys()
            for input_name in self.override.inputs:
                if input_name not in step_inputs:
                    lint_result.add_error(
                        f"{error_prefix}: input {input_name} does not exist in step",
                    )
            for parameter_name in self.override.parameters:
                if parameter_name not in step_parameters:
                    lint_result.add_error(
                        f"{error_prefix}: parameter {parameter_name} does not exist in step",
                    )

    def get_parameter_defaults(self) -> Dict[str, Any]:
        if not self.override or self.override.parameters is None:
            return {}
        return {
            name: parameter.default
            for (name, parameter) in self.override.parameters.items()
            if parameter.default is not None
        }

    def serialize(self) -> SerializedDict:
        ser = dict(super().serialize())
        if not ser.get("override"):
            ser.pop("override", None)
        return ser
