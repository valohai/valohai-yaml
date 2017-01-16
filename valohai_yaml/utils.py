from yaml import safe_load


def read_yaml(yaml):
    if isinstance(yaml, (dict, list)):  # Smells already parsed
        return yaml
    if isinstance(yaml, bytes):
        yaml = yaml.decode('utf-8')
    return safe_load(yaml)  # can be a stream or a string
