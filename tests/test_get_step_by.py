from tests.config_data import echo_step, list_step
from valohai_yaml.objs import Config


def test_get_step_by_simple_name():
    config = Config.parse([echo_step, list_step])
    assert list_step["step"] == config.get_step_by(name="list files").serialize()


def test_get_step_by_name_doesnt_exist():
    config = Config.parse([echo_step, list_step])
    assert not config.get_step_by(name="not found")


def test_get_step_by_command():
    config = Config.parse([echo_step, list_step])
    assert (
        echo_step["step"] == config.get_step_by(command="echo HELLO WORLD").serialize()
    )
    assert list_step["step"] == config.get_step_by(command="ls").serialize()


def test_get_step_by_index():
    config = Config.parse([echo_step, list_step])
    assert list_step["step"] == config.get_step_by(index=1).serialize()


def test_get_step_by_too_big_index():
    config = Config.parse([echo_step, list_step])
    assert not config.get_step_by(index=2)


def test_get_step_by_name_and_command():
    config = Config.parse([echo_step, list_step])
    assert not config.get_step_by(name="greeting", command="echo HELLO MORDOR")
    assert not config.get_step_by(name="farewell", command="echo HELLO WORLD")
    assert (
        echo_step["step"]
        == config.get_step_by(name="greeting", command="echo HELLO WORLD").serialize()
    )


def test_get_step_by_non_existing_attribute():
    config = Config.parse([echo_step, list_step])
    assert not config.get_step_by(gorilla="greeting")


def test_get_step_by_nothing_returns_none():
    config = Config.parse([echo_step, list_step])
    assert not config.get_step_by()


def test_get_step_from_empty_config():
    config = Config.parse([])
    assert not config.get_step_by(name="greeting")
