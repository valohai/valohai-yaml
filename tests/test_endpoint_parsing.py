def test_server_endpoint_parse(endpoint_config):
    endpoint = endpoint_config.endpoints["server-endpoint"]
    assert endpoint.image == "python:3.6"
    assert endpoint.port == 1453
    assert endpoint.server_command == "python run_server.py"


def test_wsgi_endpoint_parse(endpoint_config):
    endpoint = endpoint_config.endpoints["wsgi-endpoint"]
    assert endpoint.description == "predict digits from image inputs"
    assert endpoint.image == "tensorflow/tensorflow:1.3.0-py3"
    assert endpoint.wsgi == "predict_wsgi:predict_wsgi"
    assert len(endpoint.files) == 1
    file = endpoint.files[0]
    assert file.name == "model"
    assert file.description == "Model output file from TensorFlow"
    assert file.path == "model.pb"


def test_limited_endpoint_parse(endpoint_config):
    endpoint = endpoint_config.endpoints["limited-endpoint"]
    assert endpoint.resources["cpu"]["min"] == 0.1
    assert endpoint.resources["cpu"]["max"] == 1.0
    assert endpoint.resources["memory"]["min"] == 50
    assert endpoint.resources["memory"]["max"] == 100


def test_accelerated_endpoint_parse(endpoint_config):
    endpoint = endpoint_config.endpoints["accelerated-endpoint"]
    assert endpoint.node_selector == "accelerator=tesla-v100"
    assert endpoint.resources["devices"]["nvidia.com/gpu"] == 1
