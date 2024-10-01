def test_parameter_order_is_retained(keep_order_config):
    step = keep_order_config.steps["sing a melody"]
    assert list(step.parameters.keys()) == ["do", "re", "mi", "fa", "so", "la", "ti"]


def test_input_order_is_retained(keep_order_config):
    step = keep_order_config.steps["sing a melody"]
    assert list(step.inputs.keys()) == ["drums", "bass", "guitar", "vocals"]
