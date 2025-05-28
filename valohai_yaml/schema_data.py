SCHEMATA = {}


def register(schema: dict) -> None:
    SCHEMATA[schema["$id"]] = schema


register(
    {
        "$id": "https://valohai.com/schemas/base",
        "items": {
            "properties": {
                "endpoint": {"$ref": "/schemas/endpoint"},
                "pipeline": {"$ref": "/schemas/pipeline"},
                "step": {"$ref": "/schemas/step"},
                "task": {"$ref": "/schemas/task"},
            },
            "type": "object",
        },
        "type": "array",
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/deployment-node",
        "additionalProperties": False,
        "properties": {
            "actions": {"items": {"$ref": "/schemas/node-action"}, "type": "array"},
            "aliases": {"items": {"type": "string"}, "type": "array"},
            "deployment": {"type": "string"},
            "endpoints": {"items": {"type": "string"}, "type": "array"},
            "name": {"type": "string"},
            "on-error": {"enum": ["stop-all", "stop-next", "continue"], "type": "string"},
            "type": {"const": "deployment", "type": "string"},
        },
        "required": ["name", "deployment", "type"],
        "title": "DeploymentNode",
        "type": "object",
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/endpoint",
        "additionalProperties": False,
        "oneOf": [{"required": ["server-command"]}, {"required": ["wsgi"]}],
        "properties": {
            "description": {"type": "string"},
            "files": {
                "description": "Files that will be loaded into the image, for example the trained model.",
                "items": {"$ref": "/schemas/file-item"},
                "type": "array",
            },
            "image": {"description": "Docker image used to run the deployment code in.", "type": "string"},
            "name": {
                "description": "Name of the endpoint, which is used as part of the URL (i.e. "
                "/project/version/name) of the deployed endpoint. Endpoint names must be "
                "lowercase, start with a letter and may contain letters, numbers and dashes "
                "thereafter.",
                "pattern": "^[a-z][a-z0-9-]+$",
                "type": "string",
            },
            "node-selector": {
                "description": "Kubernetes node selector specifies which nodes the deployment should be scheduled to.",
                "pattern": "=",
                "type": "string",
            },
            "port": {
                "description": "Port used for the HTTP server. Defaults to 8000.",
                "maximum": 65535,
                "minimum": 1025,
                "type": "number",
            },
            "resources": {
                "additionalProperties": False,
                "description": "Resource requirements and limits for the endpoint.",
                "properties": {
                    "cpu": {"$ref": "/schemas/workflow-resource-cpu"},
                    "devices": {"$ref": "/schemas/workflow-resource-devices"},
                    "memory": {"$ref": "/schemas/workflow-resource-memory"},
                },
                "type": "object",
            },
            "server-command": {
                "description": "Command that runs a HTTP server.",
                "oneOf": [{"type": "string"}, {"items": {"type": "string"}, "type": "array"}],
            },
            "tolerations": {
                "description": "List of Kubernetes tolerations specifying which node taints the "
                "endpoint should tolerate.",
                "items": {"$ref": "/schemas/toleration"},
                "type": "array",
            },
            "wsgi": {
                "description": "Specifies the WSGI application to serve (e.g. a Flask application). Specify "
                "the module (i.e. `package.app`) or the module and the WSGI callable (i.e. "
                "`package.app:wsgi_callable`).",
                "type": "string",
            },
        },
        "required": ["name", "image"],
        "type": "object",
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/environment-variable-item",
        "additionalProperties": False,
        "properties": {
            "default": {"description": "The default value for the environment variable.", "type": "string"},
            "description": {
                "description": "Describes the environment variable's meaning. This can be shown as a "
                "help text in the user interface.",
                "type": "string",
            },
            "name": {"description": "The environment variable. This must be unique within a Step.", "type": "string"},
            "optional": {
                "default": True,
                "description": "Whether this environment variable is optional.\n"
                "All environment variables are optional by default.\n"
                "Executions may not be created unless all required environment variables "
                "have a value, configured either explicitly in the step or trickled down from "
                "project-level settings.",
                "type": "boolean",
            },
        },
        "required": ["name"],
        "type": "object",
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/execution-node",
        "additionalProperties": False,
        "properties": {
            "actions": {"items": {"$ref": "/schemas/node-action"}, "type": "array"},
            "edge-merge-mode": {"$ref": "/schemas/node-edge-merge-mode"},
            "name": {"type": "string"},
            "on-error": {"enum": ["stop-all", "stop-next", "continue", "retry"], "type": "string"},
            "override": {"$ref": "/schemas/overridden-properties"},
            "step": {"type": "string"},
            "type": {"const": "execution", "type": "string"},
        },
        "required": ["name", "step", "type"],
        "title": "ExecutionNode",
        "type": "object",
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/file-item",
        "additionalProperties": False,
        "properties": {
            "description": {"description": "The description of the file.", "type": "string"},
            "name": {"description": "The symbolic name of this file.", "type": "string"},
            "path": {
                "description": "Relative path of the file from the endpoint's working directory. For example "
                '"data/serialized_model.hdf5".',
                "type": "string",
            },
        },
        "required": ["name", "path"],
        "type": "object",
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/input-item",
        "additionalProperties": False,
        "properties": {
            "default": {
                "description": "The default URL(s) for the input.",
                "oneOf": [{"type": "string"}, {"items": {"type": "string"}, "type": "array"}],
            },
            "description": {
                "description": "Describes the input. This is shown as a help text in the user interface.",
                "type": "string",
            },
            "download": {
                "default": "always",
                "description": "Select downloading intention for this input. On-demand inputs are not "
                "downloaded before the step can run, instead are available to download using an "
                "authenticated download URL.",
                "enum": ["always", "on-demand"],
                "type": "string",
            },
            "filename": {
                "description": "Force a filename for this input. Will not have an effect if there are "
                "multiple files for this input.",
                "type": "string",
            },
            "keep-directories": {
                "default": False,
                "description": "Whether to retain directories when using wildcards for this input.",
                "oneOf": [{"type": "boolean"}, {"enum": ["none", "full", "suffix"], "type": "string"}],
            },
            "name": {
                "description": "The symbolic name of this input. This must be unique within a Step.",
                "maxLength": 64,
                "type": "string",
            },
            "optional": {
                "default": False,
                "description": "Whether this input is optional.\n"
                "Optional inputs may be disabled in the user interface.",
                "type": "boolean",
            },
        },
        "required": ["name"],
        "type": "object",
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/mount-item",
        "anyOf": [
            {
                "description": "A simple source:destination mount string. Note both parts must be absolute.",
                "pattern": "^/.+:/.+$",
                "type": "string",
            },
            {
                "additionalProperties": False,
                "properties": {
                    "destination": {"description": "Container path for data", "pattern": "^/.+$", "type": "string"},
                    "options": {"description": "Additional mount options", "type": "object"},
                    "readonly": {
                        "default": False,
                        "description": "Whether to mount the volume read-only",
                        "type": "boolean",
                    },
                    "source": {
                        "description": "Host path for data (for local sources; for non-local mount types, depends)",
                        "type": "string",
                    },
                    "type": {"description": "Mount type", "type": "string"},
                },
                "required": ["source", "destination"],
                "type": "object",
            },
        ],
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/node-action",
        "additionalProperties": False,
        "properties": {
            "if": {"oneOf": [{"type": "string"}, {"items": {"type": "string"}, "type": "array"}]},
            "then": {"oneOf": [{"type": "string"}, {"items": {"type": "string"}, "type": "array"}]},
            "when": {"oneOf": [{"type": "string"}, {"items": {"type": "string"}, "type": "array"}]},
        },
        "required": ["when", "then"],
        "title": "NodeAction",
        "type": "object",
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/node-edge-merge-mode",
        "default": "replace",
        "description": "Whether to replace the values set for this input, "
        "or to append to them when overridden by e.g. a pipeline edge.",
        "enum": ["replace", "append"],
        "type": "string",
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/output-item",
        "additionalProperties": False,
        "properties": {
            "description": {"description": "Describes the output.", "type": "string"},
            "name": {
                "description": "The symbolic name of this output. This must be unique within a Step.",
                "type": "string",
            },
        },
        "required": ["name"],
        "type": "object",
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/overridden-properties",
        "additionalProperties": False,
        "properties": {
            "command": {
                "description": "The command or commands to run.",
                "oneOf": [{"type": "string"}, {"items": {"type": "string"}, "type": "array"}],
            },
            "environment": {
                "description": "Default execution environment (ID or substring of environment name)",
                "type": "string",
            },
            "environment-variables": {
                "description": "Environment variables and their default values for the node.",
                "items": {"$ref": "/schemas/environment-variable-item"},
                "type": "array",
            },
            "image": {"description": "The Docker image to use for this node.", "type": "string"},
            "inputs": {
                "description": "The inputs expected by the node.",
                "items": {"$ref": "/schemas/input-item"},
                "type": "array",
            },
            "mounts": {
                "description": "Custom mounts to enable, for private environments allowing them.",
                "items": {"$ref": "/schemas/mount-item"},
                "type": "array",
            },
            "parameters": {
                "description": "The parameter definitions and default values to be interpolated into the command.",
                "items": {"$ref": "/schemas/param-item"},
                "type": "array",
            },
        },
        "type": "object",
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/param-item",
        "additionalProperties": False,
        "properties": {
            "category": {
                "description": "Free-form category for the parameter. Shown in the user interface.",
                "type": "string",
            },
            "choices": {
                "description": "If choices are set, the user may only choose from these choices for the parameter.\n"
                "Not applicable to flag parameters.",
                "type": "array",
            },
            "default": {"description": "The default value for the parameter."},
            "description": {
                "description": "Describes the parameter. This is shown as a help text in the user interface.",
                "type": "string",
            },
            "max": {
                "description": "The maximum accepted value for the parameter.\n"
                "Only applicable to integer/float parameters.",
                "type": "number",
            },
            "min": {
                "description": "The minimum accepted value for the parameter.\n"
                "Only applicable to integer/float parameters.",
                "type": "number",
            },
            "multiple": {
                "default": "none",
                "description": "Whether to allow multiple values for this parameter, and how to pass them on the "
                "command line. Parameters set to `repeat` will be repeated using the `--pass-as` "
                "pattern, while `separate` will interpolate all values into a single `--pass-as` value "
                "placeholder using the `multiple-separator`.\n"
                "`multiple` is not available for flag parameters.",
                "enum": ["none", "repeat", "separate"],
                "type": "string",
            },
            "multiple-separator": {
                "default": ",",
                "description": "The separator to use when interpolating multiple values into a command parameter.\n"
                "Defaults to a comma.",
                "type": "string",
            },
            "name": {
                "description": "The symbolic name of this parameter. This must be unique within a Step.",
                "type": "string",
            },
            "optional": {
                "default": False,
                "description": "Whether this parameter is optional.\n"
                "Optional parameters may be disabled in the user interface.\n"
                "Not applicable to flag parameters; they're always optional in a sense.",
                "type": "boolean",
            },
            "pass-as": {
                "default": "--{name}={value}",
                "description": "How to pass the parameter to the command."
                "Defaults to `--{name}={value}` (or `--{name}` for flags).",
                "type": "string",
            },
            "pass-false-as": {
                "description": "How to pass flag (boolean) parameters when the flag is false."
                "If either pass-true-as or pass-false-as are set, pass-as is not used.\n",
                "type": "string",
            },
            "pass-true-as": {
                "description": "How to pass flag (boolean) parameters when the flag is true."
                "If either pass-true-as or pass-false-as are set, pass-as is not used.",
                "type": "string",
            },
            "type": {
                "default": "string",
                "description": "The type of the parameter.",
                "enum": ["flag", "float", "integer", "string"],
                "type": "string",
            },
            "widget": {
                "description": "UI widget used for editing parameter values",
                "oneOf": [
                    {
                        "properties": {"settings": {"type": "object"}, "type": {"type": "string"}},
                        "required": ["type"],
                        "type": "object",
                    },
                    {"type": "string"},
                ],
            },
        },
        "required": ["name"],
        "type": "object",
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/pipeline",
        "additionalProperties": False,
        "properties": {
            "edges": {
                "items": {
                    "anyOf": [
                        {
                            "items": False,
                            "prefixItems": [{"type": "string"}, {"type": "string"}],
                            "title": "ShorthandEdge",
                            "type": "array",
                        },
                        {
                            "additionalProperties": False,
                            "properties": {
                                "configuration": {"type": "object"},
                                "source": {"type": "string"},
                                "target": {"type": "string"},
                            },
                            "required": ["source", "target"],
                            "title": "FullEdge",
                            "type": "object",
                        },
                    ],
                },
                "type": "array",
            },
            "name": {"type": "string"},
            "nodes": {
                "items": {
                    "anyOf": [
                        {"$ref": "/schemas/execution-node"},
                        {"$ref": "/schemas/deployment-node"},
                        {"$ref": "/schemas/task-node"},
                    ],
                },
                "type": "array",
            },
            "parameters": {"items": {"$ref": "/schemas/pipeline-param"}, "type": "array"},
            "reuse-executions": {
                "default": False,
                "description": "Set to true to allow Valohai to automatically detect if the executions in"
                "steps' nodes could be skipped and reuse the result from a previously successfully run node.\n"
                "Node's execution is considered unchanged when the step's data doesn't change "
                "(inputs, command, commit hash, parameters, step's configuration).",
                "type": "boolean",
            },
        },
        "required": ["edges", "name", "nodes"],
        "title": "Pipeline Blueprint",
        "type": "object",
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/pipeline-param",
        "additionalProperties": False,
        "properties": {
            "category": {
                "description": "Free-form category for the parameter. Shown in the user interface.",
                "type": "string",
            },
            "default": {"description": "The default value for the pipeline parameter."},
            "description": {
                "description": "Describes the parameter. This is shown as a help text in the user interface.",
                "type": "string",
            },
            "name": {"type": "string"},
            "target": {"type": "string"},
            "targets": {"oneOf": [{"type": "string"}, {"items": {"type": "string"}, "type": "array"}]},
        },
        "title": "Pipeline Parameter",
        "type": "object",
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/step",
        "additionalProperties": False,
        "properties": {
            "category": {"description": "Category name to group & organize steps in the UI", "type": "string"},
            "command": {
                "description": "The command or commands to run.",
                "oneOf": [{"type": "string"}, {"items": {"type": "string"}, "type": "array"}],
            },
            "description": {
                "description": "Describes the step. This is shown as a help text in the user interface.",
                "type": "string",
            },
            "environment": {
                "description": "Default execution environment (ID or substring of environment name)",
                "type": "string",
            },
            "environment-variable-groups": {
                "description": "Groups of environment variables to include in the step execution.",
                "items": {"type": "string"},
                "type": "array",
            },
            "environment-variables": {
                "description": "Environment variables and their default values for the step.",
                "items": {"$ref": "/schemas/environment-variable-item"},
                "type": "array",
            },
            "icon": {"description": "URL to the icon representing the step", "type": "string"},
            "image": {"description": "The Docker image to use for this step.", "type": "string"},
            "inputs": {
                "description": "The inputs expected by the step.",
                "items": {"$ref": "/schemas/input-item"},
                "type": "array",
            },
            "mounts": {
                "description": "Custom mounts to enable, for private environments allowing them.",
                "items": {"$ref": "/schemas/mount-item"},
                "type": "array",
            },
            "name": {"description": "The unique name for this step.", "type": "string"},
            "no-output-timeout": {
                "description": "The time after which the step is considered to have died if no "
                'output has been generated (in seconds or as a string (e.g. "1h 30m 5s")). '
                'An unspecified value means "platform default".',
                "oneOf": [{"type": "integer"}, {"type": "string"}],
            },
            "outputs": {
                "description": "The outputs expected to be generated by the step.",
                "items": {"$ref": "/schemas/output-item"},
                "type": "array",
            },
            "parameters": {
                "description": "The parameter definitions and default values to be interpolated into the command.",
                "items": {"$ref": "/schemas/param-item"},
                "type": "array",
            },
            "resources": {
                "additionalProperties": False,
                "description": "Resource requirements and limits for the workflow.",
                "properties": {
                    "cpu": {"$ref": "/schemas/workflow-resource-cpu"},
                    "devices": {"$ref": "/schemas/workflow-resource-devices"},
                    "memory": {"$ref": "/schemas/workflow-resource-memory"},
                },
                "type": "object",
            },
            "source-path": {
                "description": "The original source file that this step comes from, relative to this config file.",
                "type": "string",
            },
            "stop-condition": {"type": "string"},
            "time-limit": {
                "description": 'The time limit for the step (in seconds or as a string, e.g. "1h 30m 5s"). '
                'An unspecified value means "no timeout".',
                "oneOf": [{"type": "integer"}, {"type": "string"}],
            },
            "upload-store": {"description": "The output data store name or UUID.", "maxLength": 64, "type": "string"},
        },
        "required": ["command", "name", "image"],
        "type": "object",
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/task",
        "additionalProperties": False,
        "properties": {
            "description": {
                "description": "Describes the task. This is shown as a help text in the user interface.",
                "type": "string",
            },
            "engine": {"type": "string"},
            "execution-batch-size": {"type": "integer"},
            "execution-count": {"type": "integer"},
            "maximum-queued-executions": {"type": "integer"},
            "name": {"description": "The unique name for this task.", "type": "string"},
            "on-child-error": {"type": "string"},
            "optimization-target-metric": {"type": "string"},
            "optimization-target-value": {"type": "number"},
            "parameter-sets": {
                "description": "Parameter sets for manual search mode.",
                "items": {"type": "object"},
                "type": "array",
            },
            "parameters": {
                "description": "The variant parameter definitions and default values to be interpolated "
                "into the command.",
                "items": {"$ref": "/schemas/variant-param"},
                "type": "array",
            },
            "step": {"description": "The step to run with.", "type": "string"},
            "stop-condition": {"type": "string"},
            "type": {"type": "string"},
        },
        "required": ["name", "step", "parameters"],
        "type": "object",
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/task-node",
        "additionalProperties": False,
        "properties": {
            "actions": {"items": {"$ref": "/schemas/node-action"}, "type": "array"},
            "edge-merge-mode": {"$ref": "/schemas/node-edge-merge-mode"},
            "name": {"type": "string"},
            "on-error": {"enum": ["stop-all", "stop-next", "continue"], "type": "string"},
            "override": {"$ref": "/schemas/overridden-properties"},
            "step": {"type": "string"},
            "type": {"const": "task", "type": "string"},
        },
        "required": ["name", "step", "type"],
        "title": "TaskNode",
        "type": "object",
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/toleration",
        "additionalProperties": False,
        "oneOf": [{"required": ["key"]}, {"properties": {"key": {"not": {}}, "operator": {"const": "Exists"}}}],
        "properties": {
            "effect": {
                "description": "Optional, empty tolerates all effects.",
                "enum": ["PreferNoSchedule", "NoSchedule", "NoExecute"],
                "type": "string",
            },
            "key": {"description": 'Optional if operator is "Exists", to match all keys.', "type": "string"},
            "operator": {
                "description": 'Optional, empty means "Equal".',
                "enum": ["Exists", "Equal"],
                "type": "string",
            },
            "value": {
                "description": 'Optional as empty in some contexts like when operator is "Exists".',
                "type": "string",
            },
        },
        "type": "object",
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/variant-param",
        "additionalProperties": False,
        "properties": {
            "name": {"type": "string"},
            "rules": {"$ref": "/schemas/variant-param-rule-item"},
            "style": {"enum": ["linear", "logspace", "multiple", "random", "single"], "type": "string"},
        },
        "required": ["name", "rules", "style"],
        "type": "object",
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/variant-param-rule-item",
        "additionalProperties": False,
        "properties": {
            "base": {"type": "number"},
            "count": {"type": "number"},
            "distribution": {"type": "string"},
            "end": {"type": "number"},
            "integerify": {"type": "boolean"},
            "items": {"items": {"type": "number"}, "type": "array"},
            "max": {"type": "number"},
            "min": {"type": "number"},
            "numberify": {"type": "boolean"},
            "seed": {"type": "number"},
            "start": {"type": "number"},
            "step": {"type": "number"},
            "value": {"type": "number"},
        },
        "type": "object",
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/workflow-resource-cpu",
        "additionalProperties": False,
        "description": "CPU resource requirements and limits in vCPU counts e.g. 0.1 is 10% of one CPU.",
        "properties": {"max": {"type": "number"}, "min": {"type": "number"}},
        "type": "object",
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/workflow-resource-devices",
        "description": "Devices required e.g. 'nvidia.com/gpu: 1' for one NVIDIA GPU.",
        "patternProperties": {"^.+$": {"minimum": 1, "type": "number"}},
        "type": "object",
    },
)
register(
    {
        "$id": "https://valohai.com/schemas/workflow-resource-memory",
        "additionalProperties": False,
        "description": "Memory requirements and limits in MB e.g. 100 is 100 MB.",
        "properties": {"max": {"type": "number"}, "min": {"type": "number"}},
        "type": "object",
    },
)

del register
