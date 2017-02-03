class _SimpleObject(object):

    def get_data(self):
        """
        Get data for serialization.
        """
        return vars(self).copy()

    def serialize(self):
        return {key.replace('_', '-'): value for (key, value) in self.get_data().items() if value is not None}

    @classmethod
    def parse(cls, data):
        return cls(**{key.replace('-', '_'): value for (key, value) in data.items()})
