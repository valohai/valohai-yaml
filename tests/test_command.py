from collections import defaultdict

from valohai_yaml.commands import build_command, join_command
from valohai_yaml.objs.parameter_map import ParameterMap


def test_command_generation(example1_config):
    config = example1_config
    step = config.steps["run training"]
    command = step.build_command(
        {
            "decoder-spec": 'foo bar""\'"\'"; quux',
        },
    )
    command = " && ".join(command)
    # Check that, uh, things, are, um, quoted.
    assert "--decoder-spec 'foo bar\"\"'\"'\"'\"'\"'\"'\"; quux'" in command
    # Check that the params are serialized in order
    last_offset = 0
    for param_name in step.parameters:
        try:
            param_offset = command.index(param_name)
        except ValueError:  # not found? ok.
            continue
        assert param_offset > last_offset
        last_offset = param_offset
    assert last_offset  # (test that the in-order test actually did something)


def test_command_override(example1_config):
    config = example1_config
    step = config.steps["run training"]
    command = step.build_command({"decoder-spec": "hello"}, command="asdf {params}")
    command = " && ".join(command)
    assert command.startswith("asdf")
    assert "--decoder-spec hello" in command


def test_nonexistent_interpolation_keys():
    empty_parameter_map = ParameterMap(parameters={}, values={})
    interp_command = build_command(
        ["Where are the ${shell_unicorns}? The {parameters} are here!"],
        empty_parameter_map,
    )
    assert interp_command == ["Where are the ${shell_unicorns}? The  are here!"]


def test_interpolate_special():
    empty_parameter_map = ParameterMap(parameters={}, values={})
    interp_command = build_command(
        ["python {source-path}"],
        empty_parameter_map,
        special_interpolations={
            "source-path": "foo.py",
        },
    )
    assert interp_command == ["python foo.py"]


parameter_test_values = {
    "decoder-spec": "hello",
    "num-epochs": 840,
}


def test_parameter_interpolation(example1_config):
    config = example1_config
    step = config.steps["run training"]
    command = step.build_command(
        parameter_values=parameter_test_values,
        command="asdf {parameter:decoder-spec} {parameter:hello} {parameter:decoder-spec}",
    )
    command = " && ".join(command)
    assert command == "asdf --decoder-spec hello {parameter:hello} --decoder-spec hello"


def test_parameter_value_interpolation(example1_config):
    config = example1_config
    step = config.steps["run training"]
    command = step.build_command(
        parameter_values=parameter_test_values,
        command=[
            "asdf {parameter-value:decoder-spec} {parameter-value:hello} {parameter-value:decoder-spec}",
            "dsfargeg {parameter-value:num-epochs}",
            "{parameter-value:decoder-spec}",
        ],
    )
    command = " && ".join(command)
    assert command == "asdf hello {parameter-value:hello} hello && dsfargeg 840 && hello"


def test_parameter_value_with_falsy_values(example1_config):
    command = example1_config.steps["run training"].build_command(
        parameter_values={
            "decoder-spec": "",
            "num-epochs": 0,
        },
        command=[
            "env ds={parameter-value:decoder-spec} eps={parameter-value:num-epochs} runrunrun",
        ],
    )
    assert command[0] == "env ds='' eps=0 runrunrun"


def test_parameter_omit_with_none_value(example1_config):
    command = example1_config.steps["run training"].build_command(
        parameter_values={
            "num-epochs": None,
        },
        command=[
            "echo {parameters}; echo {parameter:num-epochs}",
        ],
    )
    assert "num-epochs" not in command[0]


def test_parameter_categories(example1_config):
    pbc = defaultdict(set)
    for param in example1_config.steps["run training"].parameters.values():
        pbc[param.category].add(param.name)
    assert pbc == {
        None: {
            "decoder-spec",
            "denoising-cost-x",
            "encoder-layers",
            "num-epochs",
            "seed",
        },
        "Database": {"sql-query"},
        "Output": {"output-alias"},
        "Samples": {"unlabeled-samples", "labeled-samples"},
    }


def test_shebang(shebang_example_config):
    for step in shebang_example_config.steps.values():
        command = step.build_command(parameter_values={"wibble": 42})
        command = join_command(command, " && ")
        assert command.startswith("#!/bin/bash\n")
        assert "--wibble=42" in command


def test_join_command():
    assert join_command(["foo"], " && ") == "foo"
    assert join_command(["foo", " ", "bar"], " && ") == "foo && bar"
    assert join_command(["foo", " ", "bar"], "\n") == "foo\nbar"
    assert join_command(["#!/bin/sh", "foo", " ", "bar"], " && ") == "#!/bin/sh\nfoo && bar"
    assert join_command(["#!/bin/sh\nfoo", " ", "bar"], " && ") == "#!/bin/sh\nfoo && bar"
    assert join_command(["#!/bin/bash\nfoo", "#!woop"], " && ") == "#!/bin/bash\nfoo && #!woop"
