from typing import Any, Dict, List, Union

from valohai_yaml.objs import (
    Config,
    DeploymentNode,
    ExecutionNode,
    Node,
    Pipeline,
    TaskNode,
)
from valohai_yaml.utils import listify

ConvertedObject = Dict[str, Any]


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

    def convert_pipeline(self, pipeline: Pipeline) -> Dict[str, List[ConvertedObject]]:
        return {
            "edges": [edge.get_expanded() for edge in pipeline.edges],
            "nodes": [self.convert_node(node) for node in pipeline.nodes],
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

    def convert_executionlike_node(self, node: Union[ExecutionNode, TaskNode]) -> ConvertedObject:
        node_data = node.serialize()
        step_name = node_data.pop("step")
        override = node_data.pop("override", {})
        step = self.config.get_step_by(name=step_name)
        if not step:  # pragma: no cover
            raise ValueError(f"Step {step_name} not found in {self.config}")
        step_data = step.serialize()
        step_data.update(override)  # TODO: this might need to e.g. merge mappings
        step_data["parameters"] = step.get_parameter_defaults(include_flags=True)
        step_data["inputs"] = {
            i["name"]: listify(i.get("default")) for i in step_data.get("inputs", [])
        }
        step_data.pop("mounts", None)
        node_data["template"] = {
            "commit": self.commit_identifier,
            "step": step_name,
            **step_data,
        }
        return node_data
