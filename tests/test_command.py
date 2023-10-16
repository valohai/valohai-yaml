from valohai_yaml.commands import build_command
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
    assert (
        command == "asdf hello {parameter-value:hello} hello && dsfargeg 840 && hello"
    )


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
