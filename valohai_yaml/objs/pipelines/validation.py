from __future__ import annotations

from typing import TYPE_CHECKING

from valohai_yaml.lint import LintResult
from valohai_yaml.types import LintContext

if TYPE_CHECKING:
    from valohai_yaml.objs.pipelines.execution_node import ExecutionNode
    from valohai_yaml.objs.pipelines.task_node import TaskNode


def lint_step_reference(
    node: ExecutionNode | TaskNode,
    step_name: str,
    lint_result: LintResult,
    context: LintContext,
) -> None:
    config = context["config"]
    pipeline = context["pipeline"]
    error_prefix = f'Pipeline "{pipeline.name}" node "{node.name}" step "{step_name}"'

    step = config.steps.get(step_name)
    if not step:
        lint_result.add_error(f"{error_prefix} does not exist")
        return

    if node.override is not None:
        node.override.lint(lint_result, context)

        for input_name in node.override.inputs:
            if input_name not in step.inputs:
                lint_result.add_error(
                    f"{error_prefix}: input {input_name} does not exist in step",
                )

        for param_name in node.override.parameters:
            if param_name not in step.parameters:
                lint_result.add_error(
                    f"{error_prefix}: parameter {param_name} does not exist in step",
                )
