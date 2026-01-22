from typing import Any, Dict, List, Optional, Union

from valohai_yaml.lint import LintResult
from valohai_yaml.objs.pipelines.edge_merge_mode import EdgeMergeMode
from valohai_yaml.objs.pipelines.node import ErrorAction, Node
from valohai_yaml.objs.pipelines.node_action import NodeAction
from valohai_yaml.objs.pipelines.override import Override
from valohai_yaml.objs.pipelines.validation import lint_step_reference
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
        commit: Optional[str] = None,
        actions: Optional[List[NodeAction]] = None,
        override: Optional[Union[Override, NodeOverrideDict]] = None,
        on_error: Union[str, ErrorAction] = ErrorAction.STOP_ALL,
        edge_merge_mode: EdgeMergeMode = EdgeMergeMode.REPLACE,
    ) -> None:
        super().__init__(name=name, actions=actions, on_error=on_error)
        self.step = step
        self.commit = str(commit) if commit else None
        if override is None or isinstance(override, Override):
            self.override = override
        else:
            self.override = Override.parse(override)
        self.edge_merge_mode = EdgeMergeMode.cast(edge_merge_mode)

    def lint(self, lint_result: LintResult, context: LintContext) -> None:
        super().lint(lint_result, context)
        if not self.commit:
            # We can only lint step-related things if the step is defined in
            # this configuration. If a commit is specified, and thus step comes
            # from a different YAML, we can't know that.
            lint_step_reference(self, self.step, lint_result, context)

    def get_parameter_defaults(self) -> Dict[str, Any]:
        # this function is not used by us anymore, should it be deprecated?
        # iiuc, Override.merge_with_step was introduced to replace its usage

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
