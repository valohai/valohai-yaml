echo_step = {
    "step": {
        "name": "greeting",
        "command": "echo HELLO WORLD",
        "image": "busybox",
    },
}

list_step = {
    "step": {
        "name": "list files",
        "command": "ls",
        "image": "busybox",
    },
}

endpoint_with_input = {
    "endpoint": {
        "name": "predict-digit",
        "description": "predict digits from image inputs",
        "image": "tensorflow/tensorflow:1.3.0-py3",
        "wsgi": "predict_wsgi:predict_wsgi",
        "files": [
            {
                "name": "model",
                "description": "Model output file from TensorFlow",
                "path": "model.pb",
            },
        ],
    },
}

endpoint_without_input = {
    "endpoint": {
        "name": "greet",
        "image": "python:3.6",
        "server-command": "python -m wsgiref.simple_server",
        "description": "say hello",
    },
}

complex_step = {
    "step": {
        "name": "run stuff",
        "command": "foo.py {parameters}",
        "image": "busybox",
        "inputs": [
            {
                "name": "foo",
                "default": "http://example.com/default/endpoint.zip",
            },
            {
                "name": "foo2",
                "default": "http://example.com/default/herpderp.zip",
            },
        ],
        "parameters": [
            {
                "name": "i",
                "type": "integer",
                "default": 10,
            },
            {
                "name": "f",
                "type": "float",
                "default": 3.5,
            },
            {
                "name": "s",
                "type": "string",
                "optional": True,
            },
        ],
    },
}

complex_step_alt = {
    "step": {
        "name": "run stuff",
        "command": "bar.py {parameters}",
        "image": "busybox",
        "inputs": [
            {
                "name": "foo",
                "default": "http://example.com/default/endpoint_alt.zip",
            },
            {
                "name": "bar",
                "default": "http://example.com/default/foobar.zip",
            },
        ],
        "parameters": [
            {
                "name": "i",
                "type": "integer",
                "default": 11,
            },
            {
                "name": "s",
                "type": "string",
                "optional": True,
            },
            {
                "name": "s2",
                "type": "string",
                "optional": False,
            },
        ],
    },
}

complex_steps_merged = {
    "step": {
        "name": "run stuff",
        "command": "bar.py {parameters}",
        "image": "busybox",
        "inputs": [
            {
                "name": "foo",
                "default": "http://example.com/default/endpoint_alt.zip",
            },
            {
                "name": "foo2",
                "default": "http://example.com/default/herpderp.zip",
            },
            {
                "name": "bar",
                "default": "http://example.com/default/foobar.zip",
            },
        ],
        "parameters": [
            {
                "name": "i",
                "type": "integer",
                "default": 11,
            },
            {
                "name": "f",
                "type": "float",
                "default": 3.5,
            },
            {
                "name": "s",
                "type": "string",
                "optional": True,
            },
            {
                "name": "s2",
                "type": "string",
                "optional": False,
            },
        ],
    },
}
