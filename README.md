# valohai-yaml

[![Build Status](https://travis-ci.org/valohai/valohai-yaml.svg?branch=master)](https://travis-ci.org/valohai/valohai-yaml)
[![Codecov](https://codecov.io/gh/valohai/valohai-yaml/branch/master/graph/badge.svg)](https://codecov.io/gh/valohai/valohai-yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Parses and validates `valohai.yaml` files.

Installation
------------

```
pip install valohai-yaml
```

Usage (validation)
------------------

Programmatic usage:

```python
from valohai_yaml import validate, ValidationErrors

try:
    validate(open('my_yaml.yaml'))
except ValidationErrors as errors:
    print('oh no!')
    for err in errors:
        print(err)
```

Command-line usage:

```
valohai-yaml my_yaml.yaml
echo $?  # 1 if errors, 0 if ok
```

Usage (parsing)
---------------

```python
from valohai_yaml import parse
config = parse(open('my_yaml.yaml'))
print(config.steps['cool step'].command)
```
