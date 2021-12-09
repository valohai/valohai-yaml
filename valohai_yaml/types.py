from typing import Any, Dict, IO, List, Union

YamlReadable = Union[Dict[Any, Any], List[Any], bytes, str, IO[bytes], IO[str]]
SerializedDict = Dict[str, Any]
LintResultMessage = Dict[str, Any]
LintContext = Dict[str, Any]
MountOptions = Dict[str, Any]
EdgeConfigurationDict = Dict[str, Any]
EndpointResourcesDict = Dict[str, Any]
NodeOverrideDict = Dict[str, Any]
