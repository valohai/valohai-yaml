from __future__ import unicode_literals
from collections import OrderedDict
from itertools import chain

from .step import Step


class Config(object):
    """
    Represents a `valohai.yaml` file.
    """
    def __init__(self, steps=()):
        assert all(isinstance(step, Step) for step in steps)
        self.steps = OrderedDict((step.name, step) for step in steps)

    @classmethod
    def parse(cls, data):
        """
        Parse a Config structure out of a Python dict (that's likely deserialized from YAML).

        :param data: Config-y dict
        :type data: dict
        :return: Config object
        :rtype: valohai_yaml.objs.Config
        """
        step_datas = [
            datum['step']
            for datum in data
            if isinstance(datum, dict) and datum.get('step')
            ]
        return cls(steps=[Step.parse(step_data) for step_data in step_datas])

    def serialize(self):
        return list(chain(
            ({'step': step.serialize()} for step in self.steps.values())
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

    def __repr__(self):
        return '<Config with %d steps: %r>' % (
            len(self.steps),
            sorted(self.steps)
        )
