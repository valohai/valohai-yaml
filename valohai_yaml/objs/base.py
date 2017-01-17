class _SimpleObject(dict):
    "Simple dict-backed object with attribute read access"

    def __getattr__(self, item):
        return self[item]

    def serialize(self):
        return dict(self)
