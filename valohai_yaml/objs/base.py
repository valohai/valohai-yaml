from valohai_yaml.objs.utils import serialize_into


class Item(object):
    """
    Base class for all objects represented in a valohai.yaml file.

    Provides basic parsing and serialization.
    """
    _original_data = None  # Possible original data dict this object was parsed from

    def get_data(self):
        """
        Get data for serialization.
        """
        data = vars(self).copy()
        data.pop('_original_data', None)
        return data

    def serialize(self):
        out = {}
        for key, value in self.get_data().items():
            if value is None:
                continue
            key = key.replace('_', '-')
            serialize_into(out, key, value)
        return out

    @classmethod
    def parse(cls, data):
        inst = cls(**{
            key.replace('-', '_'): value
            for (key, value)
            in data.items()
            if not key.startswith('_')
        })
        inst._original_data = data
        return inst

    def lint(self, lint_result, context):
        pass
