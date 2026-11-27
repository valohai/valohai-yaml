from __future__ import annotations

from typing import Any, TypedDict, Union

from valohai_yaml.objs import (
    Config,
    DeploymentNode,
    ExecutionNode,
    Node,
    Pipeline,
    PipelineParameter,
    Step,
    Task,
    TaskNode,
)
from valohai_yaml.objs.pipelines.override import Override
from valohai_yaml.utils import snake_case_keys

ConvertedObject = dict[str, Any]


class VariantExpression(TypedDict):
    """Variant expression template."""

    style: str
    rules: dict[str, Any]


ExpressionValue = Union[str, int, bool, float, VariantExpression]

# Step fields that are named differently in the API's execution template.
STEP_TO_TEMPLATE_FIELD_RENAMES = {
    "stop_condition": "stop_expression",
}


class ConvertedPipeline(TypedDict):
    """TypedDict for converted Pipeline object."""

    edges: list[ConvertedObject]
    nodes: list[ConvertedObject]
    parameters: dict[str, ConvertedObject]
    tags: list[str]


class PipelineConverter:
    """Converts pipeline objects to Valohai API payloads."""

    def __init__(
        self,
        *,
        config: Config,
        commit_identifier: str | None,
        parameter_arguments: dict[str, str | list] | None = None,
    ) -> None:
        self.config = config
        self.commit_identifier = commit_identifier
        self.parameter_arguments = parameter_arguments or {}

    def convert_pipeline(self, pipeline: Pipeline) -> ConvertedPipeline:
        return {
            "edges": [edge.get_expanded() for edge in pipeline.edges],
            "nodes": [self.convert_node(node) for node in pipeline.nodes],
            "parameters": {parameter.name: self.convert_parameter(parameter) for parameter in pipeline.parameters},
            "tags": list(pipeline.tags),
        }

    def convert_parameter(self, parameter: PipelineParameter) -> ConvertedObject:
        """Convert a pipeline parameter to a config-expression payload."""
        param_value: ExpressionValue | list[str]
        if parameter.name in self.parameter_arguments:
            param_value = self.parameter_arguments[parameter.name]
        elif parameter.default is not None:
            param_value = parameter.default
        else:
            param_value = ""

        return {
            "config": {**parameter.serialize()},
            "expression": self.convert_expression(param_value),
        }

    def convert_node(self, node: Node) -> ConvertedObject:
        if isinstance(node, (ExecutionNode, TaskNode)):
            return self.convert_executionlike_node(node)
        if isinstance(node, DeploymentNode):
            return self.convert_deployment_node(node)
        return snake_case_keys(node.serialize())  # Assume default serialization works

    def convert_deployment_node(self, node: DeploymentNode) -> ConvertedObject:
        node_data = snake_case_keys(node.serialize())
        node_data["commit"] = self.commit_identifier
        node_data["endpoint_configurations"] = {
            f"{name}": {
                "files": {},
                "enabled": True,
            }
            for name, endpoint in self.config.endpoints.items()
            if name in node.endpoints
        }
        node_data["aliases"] = node.aliases
        return node_data

    def convert_executionlike_node(
        self,
        node: ExecutionNode | TaskNode,
    ) -> ConvertedObject:
        node_data = snake_case_keys(node.serialize())
        node_data.pop("override", None)  # we'll use the actual object, not the serialization
        node_commit = node_data.pop("commit", None)

        task_name = node_data.pop("task", None)
        step_name = node_data.pop("step", None)
        task_blueprint: Task | None = None
        if task_name and not step_name:
            task_blueprint = self.config.tasks.get(task_name)
            if not task_blueprint:  # pragma: no cover
                raise ValueError(f"Task {task_name} not found in {self.config}")
            step_name = task_blueprint.step

        if not node_commit or node_commit == self.commit_identifier:
            # Local step, let's do validation and merging properly
            step = self.config.get_step_by(name=step_name)
            if not step:  # pragma: no cover
                raise ValueError(f"Step {step_name} not found in {self.config}")
            step_data = get_local_step_template_data(step, node.override)
        else:
            # This is a remote step reference, so we can't merge with the step
            step_data = get_remote_step_template_data(node.override)

        commit = node_commit or self.commit_identifier

        if not commit:  # pragma: no cover
            raise ValueError("Cannot determine commit for node")

        node_data["template"] = {
            "commit": commit,
            "step": step_name,
            **step_data,
        }

        if task_blueprint:
            apply_task_blueprint(node_data["template"], task_blueprint)

        return node_data

    def convert_expression(self, expression: ExpressionValue | list) -> ExpressionValue:
        if isinstance(expression, list):
            return VariantExpression(
                style="single",
                rules={"value": expression},
            )
        return expression


def get_local_step_template_data(step: Step, override: Override | None) -> ConvertedObject:
    """Build template data for a step available locally, merging the node's overrides into it."""
    step_data = snake_case_keys(step.serialize())
    runtime_config = step_data.setdefault("runtime_config", {})
    if "no_output_timeout" in step_data:
        runtime_config.setdefault("no_output_timeout", step_data.pop("no_output_timeout"))
    step_data.update(Override.serialize_to_template(Override.merge_with_step(override, step)))
    return finalize_template_data(step_data)


def get_remote_step_template_data(override: Override | None) -> ConvertedObject:
    """Build template data for a step not available locally; only the node's overrides are known."""
    step_data = Override.serialize_to_template(override) if override else {}
    # Don't send empty mappings, to not override a remote step's defaults with nothing
    for key in ("inputs", "parameters"):
        if not step_data.get(key):
            step_data.pop(key, None)
    return finalize_template_data(step_data)


def finalize_template_data(step_data: ConvertedObject) -> ConvertedObject:
    # Folded in after the override merge, so that a node can override the step's value.
    # `None` means "not set anywhere"; an explicit `false` is kept.
    autorestart = step_data.pop("autorestart", None)
    if autorestart is not None:
        step_data.setdefault("runtime_config", {})["autorestart"] = autorestart
    step_data = {STEP_TO_TEMPLATE_FIELD_RENAMES.get(key, key): value for key, value in step_data.items()}
    return {key: value for key, value in step_data.items() if key not in Step.METADATA_FIELDS}


def apply_task_blueprint(template: ConvertedObject, task_blueprint: Task) -> None:
    task_to_template = Task.serialize_to_template(task_blueprint)
    task_variant_parameters = task_to_template.pop("variant_parameters", None)
    task_tags = task_to_template.pop("tags", [])
    template.update(task_to_template)
    if task_variant_parameters:
        template.setdefault("parameters", {}).update(task_variant_parameters)
    if task_tags:
        template["tags"] = list(dict.fromkeys([*template.get("tags", []), *task_tags]))
