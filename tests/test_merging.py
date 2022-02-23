from tests.config_data import (
    complex_step,
    complex_step_alt,
    complex_steps_merged,
    echo_step,
)
from valohai_yaml.objs import Config


def test_merging():
    a = Config.parse([echo_step])
    b = Config.parse([complex_step])
    c = a.merge_with(b)
    assert len(c.steps) == 2
    for step in a.steps.keys() & b.steps.keys():
        assert step in c.steps


def test_merging_conflict():
    a = Config.parse([complex_step])
    b = Config.parse([complex_step_alt])
    c = a.merge_with(b)
    expected = Config.parse([complex_steps_merged])
    assert c.serialize() == expected.serialize()
