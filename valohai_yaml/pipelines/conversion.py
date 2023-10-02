from typing import Any, Dict, List, TypedDict, Union

from valohai_yaml.objs import (
    Config,
    DeploymentNode,
    ExecutionNode,
    Node,
    Pipeline,
    PipelineParameter,
    TaskNode,
)
from valohai_yaml.objs.pipelines.override import Override

ConvertedObject = Dict[str, Any]


class ConvertedPipeline(TypedDict):
    """TypedDict for converted Pipeline object."""

    edges: List[ConvertedObject]
    nodes: List[ConvertedObject]
    parameters: Dict[str, ConvertedObject]


class PipelineConverter:
    """Converts pipeline objects to Valohai API payloads."""

    def __init__(
        self,
        *,
        config: Config,
        commit_identifier: str,
    ) -> None:
        self.config = config
        self.commit_identifier = commit_identifier

    def convert_pipeline(self, pipeline: Pipeline) -> ConvertedPipeline:
        return {
            "edges": [edge.get_expanded() for edge in pipeline.edges],
            "nodes": [self.convert_node(node) for node in pipeline.nodes],
            "parameters": {
                parameter.name: self.convert_parameter(parameter)
                for parameter in pipeline.parameters
            },
        }

    def convert_parameter(self, parameter: PipelineParameter) -> ConvertedObject:
        """Convert a pipeline parameter to a config-expression payload."""
        return {
            "config": {**parameter.serialize()},
            "expression": parameter.default if parameter.default is not None else "",
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
        node: Union[ExecutionNode, TaskNode],
    ) -> ConvertedObject:
        node_data = node.serialize()
        node_data.pop(
            "override",
            {},
        )  # we'll use the actual object, not the serialization
        step_name = node_data.pop("step")
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
        step_data.pop("mounts", None)
        node_data["template"] = {
            "commit": self.commit_identifier,
            "step": step_name,
            **step_data,
        }

        return node_data
