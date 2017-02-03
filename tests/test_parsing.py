from tests.utils import config_fixture

example1_config = config_fixture('example1.yaml')
example2_config = config_fixture('example2.yaml')


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
