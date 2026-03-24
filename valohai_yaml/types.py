from typing import IO, Any, Union

YamlReadable = Union[dict[Any, Any], list[Any], bytes, str, IO[bytes], IO[str]]
SerializedDict = dict[str, Any]
LintResultMessage = dict[str, Any]
LintContext = dict[str, Any]
MountOptions = dict[str, Any]
EdgeConfigurationDict = dict[str, Any]
EndpointResourcesDict = dict[str, Any]
EndpointTolerationDict = dict[str, Any]
NodeOverrideDict = dict[str, Any]
DeploymentDefaultsDict = dict[str, Any]
