from valohai_yaml.objs import ExecutionNode


def test_get_parameter_defaults():
    override = {
        "inputs": [
            {
                "name": "input 1",
                "default": "file.txt",
            },
        ],
        "parameters": [
            {
                "name": "epochs",
                "default": 10,
                "type": "integer",
            },
            {
                "name": "learning_rate",
                "default": 0.001,
                "type": "float",
            },
        ],
    }
    node = ExecutionNode(
        name="test",
        step="test",
        override=override,
    )
    params = node.get_parameter_defaults()
    assert "epochs" in params
    assert "learning_rate" in params
    assert params["epochs"] == 10
    assert params["learning_rate"] == 0.001
    assert len(params) == 2

    # without overrides should return empty
    empty_node = ExecutionNode(
        name="test",
        step="test",
    )
    assert empty_node.get_parameter_defaults() == {}
