# valohai-yaml

[![Build Status](https://github.com/valohai/valohai-yaml/actions/workflows/ci.yml/badge.svg)](https://github.com/valohai/valohai-yaml/actions/workflows/ci.yml)
[![Codecov](https://codecov.io/gh/valohai/valohai-yaml/branch/master/graph/badge.svg)](https://codecov.io/gh/valohai/valohai-yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Parses and validates `valohai.yaml` files.

Valohai YAML files are used to define how your machine learning project workloads and pipelines are ran on the [Valohai](https://valohai.com/) ecosystem. Refer to [Valohai Documentation](https://docs.valohai.com/) to learn how to write the actual YAML files and for more in-depth usage examples.

## Installation

```bash
pip install valohai-yaml
```

## Usage

### Validation

Programmatic usage:

```python
from valohai_yaml import validate, ValidationErrors

try:
    with open('path/to/valohai.yaml') as f:
        validate(f)
except ValidationErrors as errors:
    print('oh no!')
    for err in errors:
        print(err)
```

Command-line usage:

```bash
valohai-yaml my_yaml.yaml
echo $?  # 1 if errors, 0 if ok
```

### Parsing

```python
from valohai_yaml import parse

with open('path/to/valohai.yaml') as f:
    config = parse(f)

print(config.steps['cool step'].command)
```

# Development

```bash
# setup development dependencies
make dev

# run linting and type checks
make lint

# run tests
make test
```
