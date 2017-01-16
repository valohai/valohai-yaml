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

Usage
-----

Programmatic usage:

```python
from valohai_yaml import validate

errors = validate(open('my_yaml.yaml'))
if errors:
	print('oh no')
```

Command-line usage:

```
valohai-yaml my_yaml.yaml
echo $?  # 1 if errors, 0 if ok
```
>>>>>>> 98b7e1b... Initial code
