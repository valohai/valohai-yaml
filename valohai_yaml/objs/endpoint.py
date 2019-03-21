from __future__ import unicode_literals

from .base import Item
from .file import File


class Endpoint(Item):

    def __init__(self, name, image, description=None, files=(), port=None, server_command=None, wsgi=None):
        self.name = name
        self.description = description
        self.image = image
        self.port = port
        self.server_command = server_command
        self.wsgi = wsgi

        assert all(isinstance(f, File) for f in files)
        self.files = files

    @classmethod
    def parse(cls, kwargs):
        kwargs = kwargs.copy()
        kwargs['files'] = [File.parse(f) for f in kwargs.pop('files', ())]
        return super(Endpoint, cls).parse(kwargs)
