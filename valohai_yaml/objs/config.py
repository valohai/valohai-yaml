from __future__ import unicode_literals

from collections import OrderedDict
from itertools import chain

from .step import Step
from .endpoint import Endpoint


class Config(object):
    """
    Represents a `valohai.yaml` file.
    """

    def __init__(self, steps=(), endpoints=()):
        assert all(isinstance(step, Step) for step in steps)
        self.steps = OrderedDict((step.name, step) for step in steps)
        assert all(isinstance(endpoint, Endpoint) for endpoint in endpoints)
        self.endpoints = OrderedDict((endpoint.name, endpoint) for endpoint in endpoints)

    @classmethod
    def parse(cls, data):
        """
        Parse a Config structure out of a Python dict (that's likely deserialized from YAML).

        :param data: Config-y dict
        :type data: dict
        :return: Config object
        :rtype: valohai_yaml.objs.Config
        """
        parsers = {
            'step': ([], Step.parse),
            'endpoint': ([], Endpoint.parse),
        }
        for datum in data:
            assert isinstance(datum, dict)
            for type, (items, parse) in parsers.items():
                if type in datum:
                    items.append(parse(datum[type]))
                    break
            else:
                raise ValueError('No parser for {0}'.format(datum))
        return cls(
            steps=parsers['step'][0],
            endpoints=parsers['endpoint'][0],
        )

    def serialize(self):
        return list(chain(
            ({'step': step.serialize()} for step in self.steps.values()),
            ({'endpoint': endpoint.serialize()} for endpoint in self.endpoints.values()),
        ))

    def get_step_by(self, **kwargs):
        """
        Get the first step that matches all the passed named arguments.

        Has special argument index not present in the real step.

        Usage:
            config.get_step_by(name='not found')
            config.get_step_by(index=0)
            config.get_step_by(name="greeting", command='echo HELLO MORDOR')

        :param kwargs:
        :return: Step object or None
        :rtype: valohai_yaml.objs.Step|None
        """
        if not kwargs:
            return None
        for index, step in enumerate(self.steps.values()):
            extended_step = dict(step.serialize(), index=index)
            # check if kwargs is a subset of extended_step
            if all(item in extended_step.items() for item in kwargs.items()):
                return step
        return None

    def __repr__(self):  # pragma: no cover
        return '<Config with %d steps (%r) and %d endpoints (%r)>' % (
            len(self.steps),
            sorted(self.steps),
            len(self.endpoints),
            sorted(self.endpoints),
        )
