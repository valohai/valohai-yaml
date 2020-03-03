import os
from collections import OrderedDict
from typing import Any, Dict, Optional

import yaml

from valohai_yaml import parse as yaml_parse
from valohai_yaml.objs import Config, Parameter, Step
from valohai_yaml.objs.input import Input
from valohai_yaml.utils.merge import _merge_config
from valohai_yaml.generator.consts import DEFAULT_DOCKER_IMAGE
from valohai_yaml.generator.parser import parse

ParameterDict = Dict[str, Any]
InputDict = Dict[str, str]


def generate_step(
    *,
    relative_source_path: str,
    step: str,
    image: str,
    parameters: ParameterDict,
    inputs: InputDict
) -> Step:
    config_step = Step(
        name=step, image=image, command="python %s {parameters}" % relative_source_path,
    )

    for key, value in parameters.items():
        config_step.parameters[key] = Parameter(
            name=key, type=get_parameter_type_name(key, value), default=value,
        )

    for key, value in inputs.items():
        config_step.inputs[key] = Input(name=key, default=value,)

    return config_step


def generate_config(
    *,
    relative_source_path: str,
    step: str,
    image: str,
    parameters: ParameterDict,
    inputs: InputDict
) -> Config:
    step = generate_step(
        relative_source_path=relative_source_path,
        step=step,
        image=image,
        parameters=parameters,
        inputs=inputs,
    )
    config = Config()
    config.steps[step.name] = step
    return config


def get_current_config(config_path: str) -> Optional[Config]:
    if os.path.isfile(config_path):
        with open(config_path) as f:
            return yaml_parse(f, validate=True)
    return None


def get_source_relative_path(source_path: str, config_path: str) -> str:
    """Return path of a source file relative to config file path

    :param source_path: Path of the Python source code file
    :param config_path: Path of the valohai.yaml config file
    :return: Path of the source code file relative to the config file

    Example:
        config_file_path: /herpderp/valohai.yaml
        source_file_path: /herpderp/somewhere/underneath/test.py
        return: ./somewhere/underneath/test.py

    Ultimately used for creating command with correct relative path in valohai.yaml:
        python ./somewhere/underneath/test.py {parameters}

    """
    relative_source_dir = os.path.relpath(
        os.path.dirname(os.path.abspath(source_path)),
        os.path.dirname(os.path.abspath(config_path)),
    )
    return os.path.join(relative_source_dir, os.path.basename(source_path))


def serialize_config_to_yaml(config_path: str, config: Config):
    output = config.serialize()
    with open(config_path, "w") as output_file:
        # Make yaml.dump support OrderedDict
        # https://stackoverflow.com/questions/42518067/how-to-use-ordereddict-as-an-input-in-yaml-dump-or-yaml-safe-dump
        yaml.add_representer(
            OrderedDict,
            lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items())
        )
        output_file.write(yaml.dump(output, default_flow_style=False))


def parse_config_from_source(source_path: str, config_path: str):
    with open(source_path, "r") as source_file:
        parsed = parse(source_file.read())
        if not parsed.step:
            raise ValueError("Source is missing a call to valohai.prepare()")
        relative_source_path = get_source_relative_path(source_path, config_path)
        return generate_config(
            relative_source_path=relative_source_path,
            step=parsed.step,
            image=DEFAULT_DOCKER_IMAGE,
            parameters=parsed.parameters,
            inputs=parsed.inputs,
        )


def get_updated_config(source_path: str, config_path: str) -> (Config, Config):
    """Opens the old valohai.yaml, parses source Python file and merges the resulting config to the old

    Call to valohai.prepare() will contain step name, parameters and inputs.
    We use the AST parser to parse those from the Python source code file and
    return the merged config.

    :param source_path: Path of the Python source code file
    :param config_path: Path of the valohai.yaml config file

    """
    old_config = get_current_config(config_path)
    new_config = parse_config_from_source(source_path, config_path)
    if old_config:
        new_config = _merge_config(old_config, new_config)
    return new_config


def update_yaml_from_source(source_path: str, config_path: str):
    """Updates valohai.yaml by parsing the source code file for a call to valohai.prepare()

    Call to valohai.prepare() will contain step name, parameters and inputs.
    We use the AST parser to parse those from the Python source code file and
    update (or generate) valohai.yaml accordingly.

    :param source_path: Path of the Python source code file
    :param config_path: Path of the valohai.yaml config file

    """
    old_config = get_current_config(config_path)
    new_config = get_updated_config(source_path, config_path)
    if old_config != new_config:
        serialize_config_to_yaml(config_path, new_config)


def yaml_needs_update(source_path: str, config_path: str):
    """Checks if valohai.yaml needs updating based on source Python code.

    Call to valohai.prepare() will contain step name, parameters and inputs.
    We use the AST parser to parse those from the Python source code file and
    see if valohai.yaml needs updating.

    :param source_path: Path of the Python source code file
    :param config_path: Path of the valohai.yaml config file

    """
    old_config = get_current_config(config_path)
    new_config = get_updated_config(source_path, config_path)

    if not old_config or not new_config:
        return True

    return old_config.serialize() != new_config.serialize()


def get_parameter_type_name(name: str, value: Any) -> str:
    if isinstance(value, bool):
        return "flag"
    if isinstance(value, float):
        return "float"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, str):
        return "string"

    raise ValueError(
        "Unrecognized parameter type for %s=%s. Supported Python types are float, int, string and bool."
        % (name, value)
    )
