import os

examples_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'examples'))
bad_example_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'invalid.yaml'))

valid_bytes = b'''
- step:
    name: foo
    command: foo
    image: foo
'''

invalid_obj = [
    {
        'step': {
            'nerm': 'blerp',
        }
    },
]

valid_obj = [
    {
        'step': {
            'name': 'foo',
            'command': 'foo',
            'image': 'foo',
        }
    },
]
