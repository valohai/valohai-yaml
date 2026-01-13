from __future__ import annotations

from typing import Any, Dict, MutableMapping, TypedDict, Union

from valohai_yaml.objs import (
    Config,
    DeploymentNode,
    ExecutionNode,
    Node,
    Pipeline,
    PipelineParameter,
    Task,
    TaskNode,
)
from valohai_yaml.objs.pipelines.override import Override

ConvertedObject = Dict[str, Any]


class VariantExpression(TypedDict):
    """Variant expression template."""

    style: str
    rules: dict[str, Any]


ExpressionValue = Union[str, int, bool, float, VariantExpression]


class ConvertedPipeline(TypedDict):
    """TypedDict for converted Pipeline object."""

    edges: list[ConvertedObject]
    nodes: list[ConvertedObject]
    parameters: dict[str, ConvertedObject]


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
        return node.serialize()  # Assume default serialization works

    def convert_deployment_node(self, node: DeploymentNode) -> ConvertedObject:
        node_data = node.serialize()
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
        node_data = node.serialize()
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

        step_data: MutableMapping[str, Any]
        if not node_commit or node_commit == self.commit_identifier:
            # Local step, let's do validation and merging properly
            step = self.config.get_step_by(name=step_name)
            if not step:  # pragma: no cover
                raise ValueError(f"Step {step_name} not found in {self.config}")
            step_data = step.serialize()
            runtime_config = step_data.setdefault("runtime_config", {})
            if "no-output-timeout" in step_data:
                runtime_config.setdefault(
                    "no_output_timeout",
                    step_data.pop("no-output-timeout"),
                )
            override = Override.merge_with_step(node.override, step)
            overridden_to_template = Override.serialize_to_template(override)
            step_data.update(overridden_to_template)
        else:
            # This is a remote step reference.
            # Just add in overrides and hope for the best...
            step_data = node.override.serialize() if node.override else {}

        commit = node_commit or self.commit_identifier

        if not commit:  # pragma: no cover
            raise ValueError("Cannot determine commit for node")

        node_data["template"] = {
            "commit": commit,
            "step": step_name,
            **step_data,
        }

        if task_blueprint:
            task_to_template = Task.serialize_to_template(task_blueprint)
            task_variant_parameters = task_to_template.pop("variant_parameters", None)
            node_data["template"].update(task_to_template)
            if task_variant_parameters:
                node_data["template"].setdefault("parameters", {}).update(task_variant_parameters)

        return node_data

    def convert_expression(self, expression: ExpressionValue | list) -> ExpressionValue:
        if isinstance(expression, list):
            return VariantExpression(
                style="single",
                rules={"value": expression},
            )
        return expression
