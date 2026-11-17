from pathlib import Path

_tests_dir = Path(__file__).resolve().parent

examples_path = _tests_dir.parent / "examples"
error_examples_path = _tests_dir / "error_examples"
warning_examples_path = _tests_dir / "warning_examples"
valid_examples_path = _tests_dir / "valid_examples"

example_paths = sorted(examples_path.glob("*.yaml"))
error_example_paths = sorted(error_examples_path.glob("*.yaml"))
warning_example_paths = sorted(warning_examples_path.glob("*.yaml"))
valid_example_paths = sorted(valid_examples_path.glob("*.yaml"))

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
