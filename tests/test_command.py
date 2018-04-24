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
