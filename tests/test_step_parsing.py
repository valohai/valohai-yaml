def test_parse_inputs(example2_config):
    config = example2_config
    step = config.steps['run training']
    assert len(step.inputs) == 5
    assert len([inp.description for inp in step.inputs.values() if inp.description]) == 4


def test_parse_input_defaults(example3_config):
    config = example3_config
    step = config.steps['batch inference']
    assert len(step.inputs) == 2
    assert step.inputs['model'].default == 's3://foo/model.pb'
    assert isinstance(step.inputs['images'].default, list) and len(step.inputs['images'].default) == 2


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


def test_boolean_param_parse(boolean_param_config):
    step = boolean_param_config.steps['test']
    assert step.parameters['case-insensitive'].optional
    assert step.parameters['case-insensitive'].choices == (True, False)
    assert step.parameters['defaults-to-true'].optional
    assert step.parameters['defaults-to-true'].choices == (True, False)
    assert step.build_command({'case-insensitive': True}) == ['foo --case-insensitive']
    assert step.build_command({'case-insensitive': False}) == ['foo']
    assert step.build_command({'defaults-to-true': True}) == ['foo --defaults-to-true']
    assert step.build_command({'defaults-to-true': False}) == ['foo']
    assert step.build_command({}) == ['foo']


def test_optional_default_param_parse(optional_default_param_config):
    step = optional_default_param_config.steps['test']
    assert step.parameters['varA'].optional
    assert step.parameters['varA'].default == 123
    assert step.parameters['varB'].optional
    assert not step.parameters['varB'].default
    assert not step.parameters['varC'].optional
    assert step.parameters['varC'].default == 456
    assert not step.parameters['varD'].optional
    assert not step.parameters['varD'].default

    assert step.build_command({'varA': 666}) == ['foo --varA=666 --varC=456']
    assert step.build_command({'varB': 666}) == ['foo --varA=123 --varB=666 --varC=456']
    assert step.build_command({}) == ['foo --varA=123 --varC=456']


def test_mount_parse(mount_config):
    step = mount_config.steps['test']
    assert len(step.mounts) == 2


def test_parse_environment_variables(example3_config):
    config = example3_config
    step = config.steps['batch inference']
    assert {ev.name: ev.default for ev in step.environment_variables.values()} == {
        'foo': 'bar',
        'baz': '850',
    }
    assert step.environment_variables['foo'].optional
    assert not step.environment_variables['baz'].optional


def test_parse_environment(example3_config):
    config = example3_config
    step = config.steps['batch inference']
    assert step.environment == 'g2.superduperlarge'
