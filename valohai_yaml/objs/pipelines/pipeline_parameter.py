from typing import TYPE_CHECKING, List, Optional, Union

from valohai_yaml.lint import LintResult
from valohai_yaml.objs.base import Item
from valohai_yaml.objs.utils import check_type_and_listify
from valohai_yaml.types import LintContext, SerializedDict
from valohai_yaml.utils.node_socket_utils import split_socket_str

if TYPE_CHECKING:
    from valohai_yaml.objs import Config, Pipeline


class PipelineParameter(Item):
    """Represents a parameter definition within a pipeline definition."""

    def __init__(
        self,
        *,
        name: str,
        targets: Union[List[str], str],
        value: Optional[str] = None,
        default: Optional[str] = None,
    ) -> None:
        self.name = name
        self.default = default if value is None else value
        if isinstance(targets, str):
            self.targets = [targets]
        else:
            self.targets = check_type_and_listify(targets, str)

    @classmethod
    def parse(cls, data: SerializedDict) -> "PipelineParameter":
        data = data.copy()
        # targets can be a string or a list of strings
        if "target" in data:
            if "targets" in data:
                raise TypeError(
                    "Pipeline parameter cannot have both: target and targets",
                )
            data["targets"] = [data.pop("target")]
        return super().parse(data)

    def lint(self, lint_result: LintResult, context: LintContext) -> None:
        pipeline: Pipeline = context["pipeline"]
        config: Config = context["config"]
        steps = config.steps
        node_map = pipeline.node_map
        for target in self.targets:
            target_node_name, socket_type, target_parameter_name = split_socket_str(
                target,
            )
            if not socket_type.startswith("parameter"):
                lint_result.add_error(
                    f'Pipeline "{pipeline.name}" parameter "{self.name}" target "{target}": socket type "{socket_type}"'
                    f" is not supported.",
                )
            if target_node_name not in node_map:
                lint_result.add_error(
                    f'Pipeline "{pipeline.name}" parameter "{self.name}" target "{target}": the node '
                    f'"{target_node_name}" does not exist.',
                )
            else:
                node = node_map[target_node_name]
                from valohai_yaml.objs import ExecutionNode

                if isinstance(node, ExecutionNode):
                    step = steps[node.step]
                    if target_parameter_name not in step.parameters:
                        lint_result.add_error(
                            f'Pipeline "{pipeline.name}" parameter "{self.name}" target "{target}": the parameter '
                            f'"{target_parameter_name}" does not exist in step "{step.name}".',
                        )
