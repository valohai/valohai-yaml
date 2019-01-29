def test_endpoint_parse(endpoint_config):
    server_endpoint = endpoint_config.endpoints['server-endpoint']
    assert server_endpoint.image == 'python:3.6'
    assert server_endpoint.port == 1453
    assert server_endpoint.server_command == 'python run_server.py'
    wsgi_endpoint = endpoint_config.endpoints['wsgi-endpoint']
    assert wsgi_endpoint.description == 'predict digits from image inputs'
    assert wsgi_endpoint.image == 'tensorflow/tensorflow:1.3.0-py3'
    assert wsgi_endpoint.wsgi == 'predict_wsgi:predict_wsgi'
    assert len(wsgi_endpoint.files) == 1
    file = wsgi_endpoint.files[0]
    assert file.name == 'model'
    assert file.description == 'Model output file from TensorFlow'
    assert file.path == 'model.pb'
