def consume_array_of(source, key, type):
    return [type.parse(datum) for datum in source.pop(key, ())]


def serialize_into(dest, key, value, flatten_dicts=False, elide_empty_iterables=False):
    if value is None:
        return

    if flatten_dicts and isinstance(value, dict):
        value = list(value.values())

    if isinstance(value, (tuple, list)):  # can't use collections.Collection :(
        if elide_empty_iterables and not value:
            return
        value = [_serialize_if_able(item) for item in value]
    else:
        value = _serialize_if_able(value)

    dest[key] = value


def _serialize_if_able(v):
    return (v.serialize() if hasattr(v, 'serialize') else v)
