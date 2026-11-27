from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

import pytest

from tests.consts import example_paths, valid_example_paths
from valohai_yaml import parse
from valohai_yaml.pipelines.conversion import PipelineConverter
from valohai_yaml.utils.duration import parse_duration_string

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

    from valohai_yaml.objs import Config


def test_pipeline_conversion_smoke(pipeline_config: Config):
    for pipeline in pipeline_config.pipelines.values():
        result = PipelineConverter(
            config=pipeline_config,
            commit_identifier="latest",
        ).convert_pipeline(pipeline)
        assert result["nodes"]
        assert result["edges"]


def test_pipeline_conversion_override_order(pipeline_config: Config):
    result = PipelineConverter(
        config=pipeline_config,
        commit_identifier="latest",
    ).convert_pipeline(pipeline_config.pipelines["My medium pipeline"])
    train_node = next(node for node in result["nodes"] if node["name"] == "train")
    # If conversion order is incorrect, this will have remained a list
    assert isinstance(train_node["template"]["inputs"], dict)


def test_pipeline_conversion_no_output_timeout(pipeline_config: Config):
    result = PipelineConverter(
        config=pipeline_config,
        commit_identifier="latest",
    ).convert_pipeline(pipeline_config.pipelines["My medium pipeline"])
    train_node = next(node for node in result["nodes"] if node["name"] == "train")
    assert train_node["template"]["runtime_config"]["no_output_timeout"] == parse_duration_string("6h").total_seconds()


def test_pipeline_conversion_tags(tags_config: Config, pipeline_config: Config):
    result = PipelineConverter(
        config=tags_config,
        commit_identifier="latest",
    ).convert_pipeline(tags_config.pipelines["train-and-evaluate"])
    templates = {node["name"]: node["template"] for node in result["nodes"]}
    assert templates["train"]["tags"] == ["training", "team-vision"]
    assert "tags" not in templates["evaluate"]
    assert result["tags"] == ["nightly"]
    untagged = PipelineConverter(
        config=pipeline_config,
        commit_identifier="latest",
    ).convert_pipeline(pipeline_config.pipelines["My little pipeline"])
    assert untagged["tags"] == []


def test_pipeline_conversion_override_inputs(pipeline_overridden_config: Config):
    result = PipelineConverter(
        config=pipeline_overridden_config,
        commit_identifier="latest",
    ).convert_pipeline(
        pipeline_overridden_config.pipelines["My overriden input pipeline"],
    )

    merged = next(node for node in result["nodes"] if node["name"] == "merged")
    assert merged["template"]["command"][0] == "merge date"
    assert merged["template"]["image"] == "merge node image"
    assert isinstance(merged["template"]["inputs"], dict)
    assert len(merged["template"]["inputs"].get("training-images", [])) == 2
    assert merged["template"]["inputs"].get("training-images", [])[0] == "merged node image 1"
    assert len(merged["template"]["parameters"].items()) == 3

    overridden = next(node for node in result["nodes"] if node["name"] == "overridden")
    assert isinstance(overridden["template"]["inputs"], dict)
    assert overridden["template"]["inputs"].get("training-images", [])[0] == "overridden node image"
    assert len(overridden["template"]["inputs"].get("training-images", [])) == 1
    assert len(overridden["template"]["parameters"].items()) == 3


def test_pipeline_parameter_conversion(pipeline_with_parameters_config):
    for pipe in pipeline_with_parameters_config.pipelines.values():
        result = PipelineConverter(
            config=pipeline_with_parameters_config,
            commit_identifier="latest",
        ).convert_pipeline(pipe)
        for parameter_name in [param.name for param in pipe.parameters]:
            assert isinstance(result["parameters"], dict)
            assert result["parameters"][parameter_name]

            parameter = result["parameters"][parameter_name]
            assert parameter["config"]["targets"]
            assert "target" not in parameter["config"]
            assert isinstance(parameter["config"]["targets"], list)

            # When pipeline parameter has no default value, the expression should be empty
            parameter_config = next(param for param in pipe.parameters if param.name == parameter_name)
            expression_value = parameter_config.default if parameter_config.default is not None else ""
            # When pipeline parameter is list it should be converted to a variant parameter
            if isinstance(expression_value, list):
                assert parameter["expression"] == {
                    "style": "single",
                    "rules": {"value": expression_value},
                }
            else:
                assert parameter["expression"] == expression_value
                assert type(parameter["expression"]) is type(expression_value)


def test_pipeline_parameter_conversion_with_args(pipeline_with_parameters_config):
    pipeline = pipeline_with_parameters_config.pipelines["Example Pipeline with Parameters"]
    args = {
        "param0-float": 1.5,
        "param0-int": 3,
        "param0-string": "iceberg",
        "param0-flag": True,
        "listings": ["msg", "pfa"],
    }
    result = PipelineConverter(
        config=pipeline_with_parameters_config,
        commit_identifier="latest",
        parameter_arguments=args,
    ).convert_pipeline(pipeline)
    params = result["parameters"]

    assert params["param0-float"]["expression"] == 1.5
    assert params["param0-int"]["expression"] == 3
    assert params["param0-string"]["expression"] == "iceberg"
    assert params["param0-flag"]["expression"]
    assert params["listings"]["expression"] == {
        "style": "single",
        "rules": {"value": ["msg", "pfa"]},
    }


def test_pipeline_commit_conversion(pipeline_with_different_commit_config: Config):
    pipeline = pipeline_with_different_commit_config.pipelines["One Library Step, One Local Step"]
    result = PipelineConverter(
        config=pipeline_with_different_commit_config,
        commit_identifier="102dsgkmr4",
    ).convert_pipeline(pipeline)
    assert result["nodes"] == [
        {
            "name": "preprocess",
            "type": "execution",
            "template": {"commit": "library:generic-preprocessors/csv-into-parquet", "step": "parquetify"},
        },
        {
            "name": "mangle",
            "type": "execution",
            "template": {
                "commit": "102dsgkmr4",
                "step": "mangle",
                "image": "python:3.13",
                "command": "false",
                "inputs": {"mangles": []},
                "runtime_config": {},
                "parameters": {},
            },
        },
    ]


def test_pipeline_conversion_env_vars_are_dict(pipeline_with_env_vars_config: Config):
    """Pipeline node support for environment-variables."""
    pipeline = pipeline_with_env_vars_config.pipelines["Edge types showcase"]
    result = PipelineConverter(config=pipeline_with_env_vars_config, commit_identifier="abc123").convert_pipeline(
        pipeline,
    )

    node = result["nodes"][0]  # "preprocess"
    env_vars = node["template"]["environment_variables"]
    assert isinstance(env_vars, dict), "environment-variables should be a dict, not a list, for API compatibility"
    assert env_vars["DATA_VERSION"] == "v1.0"
    assert env_vars["PREPROCESS_MODE"] == "full"


def test_pipeline_conversion_autorestart_override(pipeline_with_autorestart_override: Config):
    """Node overrides decide the autorestart value of the converted template."""
    pipeline = pipeline_with_autorestart_override.pipelines["Training pipeline"]
    result = PipelineConverter(
        config=pipeline_with_autorestart_override,
        commit_identifier="abc123",
    ).convert_pipeline(pipeline)
    templates = {node["name"]: node["template"] for node in result["nodes"]}

    # step says true, override says false
    assert templates["train-node"]["runtime_config"]["autorestart"] is False
    # step does not say anything, override says true
    assert templates["predict-node"]["runtime_config"]["autorestart"] is True
    # task nodes are overridden the same way
    assert templates["train-task-node"]["runtime_config"]["autorestart"] is False
    # an override that does not mention autorestart keeps the step's value
    assert templates["inherit-node"]["runtime_config"]["autorestart"] is True
    # a remote step is not available locally, so only the override folds in
    assert templates["remote-node"]["runtime_config"]["autorestart"] is True

    # the value only lives in runtime_config, not at the top level of the template
    assert not any("autorestart" in template for template in templates.values())


def test_pipeline_conversion_emits_snake_case_keys(pipeline_api_keys_config: Config):
    """The converted payload is for the API, so YAML's kebab-case keys must become snake_case."""
    assert pipeline_api_keys_config.lint().is_valid()
    result = PipelineConverter(
        config=pipeline_api_keys_config,
        commit_identifier="abc123",
    ).convert_pipeline(pipeline_api_keys_config.pipelines["api-keys"])
    assert not list(find_kebab_case_keys(result))
    nodes = {node["name"]: node for node in result["nodes"]}

    local = nodes["local-node"]
    assert local["on_error"] == "continue"
    assert local["edge_merge_mode"] == "append"
    template = local["template"]
    assert template["runtime_config_preset"] == "other-preset"
    assert template["environment_variables"] == {"SOME_VAR": "some-value", "OTHER_VAR": "other-value"}
    assert template["environment_variable_groups"] == ["some-group"]
    assert template["time_limit"] == 300
    assert template["upload_store"] == "some-store"
    assert template["runtime_config"]["no_output_timeout"] == 3600
    # User-defined names are not mangled
    assert template["parameters"] == {"kebab-param": 1}
    assert template["inputs"] == {"kebab-input": ["s3://foo/bar.txt"]}

    # The step's stop condition goes by another name in the API
    assert template["stop_expression"] == "loss < 0.1"
    assert "stop_condition" not in template
    # Step-only metadata is not part of an execution template
    for key in ("name", "source_path", "cache_volumes", "resources", "outputs", "description"):
        assert key not in template

    # Free-form user data is passed through untouched
    assert template["mounts"][0]["options"] == {"some-option": "x"}
    assert result["edges"][0]["configuration"] == {"some-key": "x"}

    # Remote nodes can't be merged with their step, but overrides are still converted to the API's shape
    remote_template = nodes["remote-node"]["template"]
    assert remote_template["runtime_config_preset"] == "other-preset"
    assert remote_template["environment_variables"] == {"OTHER_VAR": "other-value"}
    assert remote_template["parameters"] == {"kebab-param": 2}
    assert remote_template["inputs"] == {"kebab-input": ["s3://foo/baz.txt"]}

    assert nodes["task-node"]["on_error"] == "stop-next"


# Mappings in the converted payload that are keyed by user-defined names
# (which may well contain dashes), rather than by API field names.
NAME_KEYED_MAPPINGS = {
    "endpoint_configurations",
    "environment_variables",
    "inputs",
    "parameters",
    "variant_parameters",
}

# Opaque user data passed through to the API as-is, so keys anywhere within can be anything.
OPAQUE_PATH_RE = re.compile(r"\.edges\[\d+\]\.configuration$|\.mounts\[\d+\]\.options$|\.resources\.devices$")


def find_kebab_case_keys(obj: Any, path: str = "") -> Iterator[str]:
    """Yield the paths of all kebab-case API field keys in a converted payload."""
    if OPAQUE_PATH_RE.search(path):
        return
    if isinstance(obj, dict):
        parent_key = path.rsplit(".", 1)[-1]
        for key, value in obj.items():
            if "-" in key and parent_key not in NAME_KEYED_MAPPINGS:
                yield f"{path}.{key}"
            yield from find_kebab_case_keys(value, f"{path}.{key}")
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            yield from find_kebab_case_keys(item, f"{path}[{i}]")


def _get_pipeline_example_paths() -> list[Path]:
    return [path for path in sorted([*example_paths, *valid_example_paths]) if "pipeline:" in path.read_text()]


@pytest.mark.parametrize("roundtrip", [False, True], ids=["direct", "roundtrip"])
@pytest.mark.parametrize("example_path", _get_pipeline_example_paths(), ids=lambda p: p.name)
def test_pipeline_conversion_never_emits_kebab_case_keys(example_path: Path, roundtrip: bool):
    """Regression test: converted pipelines are API payloads, so must use snake_case keys."""
    # The YAML side uses kebab-case (and `.serialize()` emits it), so it's easy to leak those
    # into the payload by accident; this checks every example pipeline we have.
    with example_path.open() as infp:
        config = parse(infp)
    if roundtrip:
        config = parse(config.serialize())
    assert config.pipelines, "Missä ovat yksisarviset?"
    for pipeline in config.pipelines.values():
        result = PipelineConverter(config=config, commit_identifier="abc123").convert_pipeline(pipeline)
        assert not list(find_kebab_case_keys(result)), f"kebab-case keys in converted pipeline {pipeline.name!r}"
