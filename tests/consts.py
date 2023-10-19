import os

examples_path = os.path.realpath(
    os.path.join(os.path.dirname(__file__), "..", "examples"),
)
error_examples_path = os.path.realpath(
    os.path.join(os.path.dirname(__file__), "error_examples"),
)
warning_examples_path = os.path.realpath(
    os.path.join(os.path.dirname(__file__), "warning_examples"),
)
valid_examples_path = os.path.realpath(
    os.path.join(os.path.dirname(__file__), "valid_examples"),
)

valid_bytes = b"""
- step:
    name: foo
    command: foo
    image: foo
- endpoint:
    name: xyz
    image: xyz
    port: 1453
    server-command: ./hs.sh
- endpoint:
    name: xyz
    image: xyz
    wsgi: hs:sh
"""

invalid_obj = [
    {
        "step": {
            "nerm": "blerp",
            "upload-store": 0,
        },
    },
]

valid_obj = [
    {
        "step": {
            "name": "foo",
            "upload-store": "foo",
            "command": "foo",
            "image": "foo",
        },
    },
    {
        "endpoint": {
            "name": "xyz",
            "image": "xyz",
            "port": 1453,
            "server-command": "./hs.sh",
        },
    },
    {
        "endpoint": {
            "name": "xyz",
            "image": "xyz",
            "wsgi": "hs:sh",
        },
    },
]
