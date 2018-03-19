import pytest

from tests.utils import config_fixture
from valohai_yaml import parse

example1_config = config_fixture('example1.yaml')
example2_config = config_fixture('example2.yaml')
boolean_param_config = config_fixture('flag-param-example.yaml')
mount_config = config_fixture('mount-example.yaml')
endpoint_config = config_fixture('endpoint-example.yaml')


def test_parse_inputs(example2_config):
    config = example2_config
    step = config.steps['run training']
    assert len(step.inputs) == 5


def test_parse(example1_config):
    config = example1_config
    # test that we can access a step by name
    step = config.steps['run training']

    # test that we parsed all params
    parameters = step.parameters
    assert len(parameters) == 7
    # test that we can access them by name
    assert parameters['seed'].default == 1
    assert parameters['decoder-spec'].default == 'gauss'
    # test that their order is preserved
    assert list(parameters) == [
        'num-epochs',
        'seed',
        'labeled-samples',
        'unlabeled-samples',
        'encoder-layers',
        'denoising-cost-x',
        'decoder-spec',
    ]

    # test that `get_step_by` works
    assert step == config.get_step_by(index=0)
    assert step == config.get_step_by(name='run training')
    assert step == config.get_step_by(image='busybox')
    assert not config.get_step_by(image='bdfaweq')
    assert not config.get_step_by()


def test_command_generation(example1_config):
    config = example1_config
    step = config.steps['run training']
    command = step.build_command({
        'decoder-spec': 'foo bar""\'"\'"; quux',
    })
    command = ' && '.join(command)
    # Check that, uh, things, are, um, quoted.
    assert "--decoder-spec \'foo bar\"\"\'\"\'\"\'\"\'\"\'\"\'\"; quux\'" in command
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
    step = config.steps['run training']
    command = step.build_command({'decoder-spec': 'hello'}, command='asdf {params}')
    command = ' && '.join(command)
    assert command.startswith('asdf')
    assert '--decoder-spec hello' in command


def test_boolean_param_parse(boolean_param_config):
    step = boolean_param_config.steps['test']
    assert step.parameters['case-insensitive'].optional
    assert step.parameters['case-insensitive'].choices == (True, False)
    assert step.build_command({'case-insensitive': True}) == ['foo --case-insensitive']
    assert step.build_command({'case-insensitive': False}) == ['foo']


def test_mount_parse(mount_config):
    step = mount_config.steps['test']
    assert len(step.mounts) == 2


def test_endpoint_parse(endpoint_config):
    server_endpoint = endpoint_config.endpoints['server-endpoint']
    assert server_endpoint.image == 'python:3.6'
    assert server_endpoint.port == 1453
    assert server_endpoint.server_command == 'python run_server.py'
    wsgi_endpoint = endpoint_config.endpoints['wsgi-endpoint']
    assert wsgi_endpoint.description == 'predict digits from image inputs'
    assert wsgi_endpoint.image == 'gcr.io/tensorflow/tensorflow:1.3.0-py3'
    assert wsgi_endpoint.wsgi == 'predict_wsgi:predict_wsgi'
    assert len(wsgi_endpoint.files) == 1
    file = wsgi_endpoint.files[0]
    assert file.name == 'model'
    assert file.description == 'Model output file from TensorFlow'
    assert file.path == 'model.pb'


def test_unknown_parse():
    with pytest.raises(ValueError) as e:
        fail_config = '[{ city_name: Constantinople }]'
        parse(fail_config)
    assert e.value.args[0] == "No parser for {'city_name': 'Constantinople'}"
