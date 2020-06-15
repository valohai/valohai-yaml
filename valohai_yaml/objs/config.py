import copy
from collections import OrderedDict
from itertools import chain
from typing import Any, Optional

from ..utils.merge import merge_simple, merge_dicts
from ..utils.lint import lint_iterables
from .base import Item
from .endpoint import Endpoint
from .pipelines.pipeline import Pipeline
from .step import Step


class Config(Item):
    """
    Represents a `valohai.yaml` file.
    """

    # Warnings that may be stuck on the top-level config during its parsing.
    _parse_warnings = None

    def __init__(
        self,
        *,
        steps=(),
        endpoints=(),
        pipelines=()
    ) -> None:
        assert all(isinstance(step, Step) for step in steps)
        self.steps = OrderedDict((step.name, step) for step in steps)
        assert all(isinstance(endpoint, Endpoint) for endpoint in endpoints)
        self.endpoints = OrderedDict((endpoint.name, endpoint) for endpoint in endpoints)
        assert all(isinstance(pipeline, Pipeline) for pipeline in pipelines)
        self.pipelines = OrderedDict((pipeline.name, pipeline) for pipeline in pipelines)

    @classmethod
    def parse(cls, data: Any) -> 'Config':
        """
        Parse a Config structure out of a Python dict (that's likely deserialized from YAML).

        :param data: Config-y dict
        :type data: dict
        :return: Config object
        :rtype: valohai_yaml.objs.Config
        """
        parsers = cls.get_top_level_parsers()
        parse_warnings = []
        for datum in data:
            assert isinstance(datum, dict)
            for type, (items, parse) in parsers.items():
                if type in datum:
                    items.append(parse(datum[type]))
                    break
            else:
                parse_warnings.append('No parser for {0}'.format(datum))
        inst = cls(
            steps=parsers['step'][0],
            endpoints=parsers['endpoint'][0],
            pipelines=parsers['pipeline'][0],
        )
        inst._original_data = data
        inst._parse_warnings = parse_warnings
        return inst

    @classmethod
    def get_top_level_parsers(cls):
        """
        Get the parsers for top-level elements in a configuration file.

        The return value is a little baroque due to the alias for `pipeline`/`blueprint`:
        it's a dict that maps top-level element names to a 2-tuple of target list objects and parse functions.
        """
        pipeline_tuple = ([], Pipeline.parse)
        return {
            'step': ([], Step.parse),
            'endpoint': ([], Endpoint.parse),
            'pipeline': pipeline_tuple,
            'blueprint': pipeline_tuple,  # Alias allowed for now
        }

    def serialize(self) -> Any:
        return list(chain(
            ({'step': step.serialize()} for (key, step) in sorted(self.steps.items())),
            ({'endpoint': endpoint.serialize()} for (key, endpoint) in sorted(self.endpoints.items())),
            ({'pipeline': pipeline.serialize()} for (key, pipeline) in sorted(self.pipelines.items())),
        ))

    def lint(self, lint_result=None, context=None):
        """
        Lint the configuration.

        :param lint_result: LintResult object. Optional; if not passed in, one is constructed.
        :param context: Optional context dictionary; should likely not be passed in at top level.
        :return: The lint result object used.
        """
        if context is None:
            context = {}
        if lint_result is None:
            from valohai_yaml.lint import LintResult
            lint_result = LintResult()
        context = dict(context, config=self)

        if self._parse_warnings:
            for warning in self._parse_warnings:
                lint_result.add_warning(warning)

        lint_iterables(lint_result, context, (
            self.steps,
            self.endpoints,
            self.pipelines,
        ))
        return lint_result

    def get_step_by(self, **kwargs) -> Optional[Step]:
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

    @classmethod
    def default_merge(cls, a, b):
        result = merge_simple(a, b)
        result.steps = merge_dicts(
            a.steps,
            b.steps,
            merger=Step.default_merge,
            copier=copy.deepcopy,
        )
        result.endpoints = merge_dicts(
            a.endpoints,
            b.endpoints,
            merger=merge_simple,
            copier=copy.deepcopy,
        )
        result.pipelines = merge_dicts(
            a.pipelines,
            b.pipelines,
            merger=merge_simple,
            copier=copy.deepcopy,
        )
        return result

    def __repr__(self):  # pragma: no cover
        return '<Config with %d steps (%r), %d endpoints (%r), and %d pipelines (%r)>' % (
            len(self.steps),
            sorted(self.steps),
            len(self.endpoints),
            sorted(self.endpoints),
            len(self.pipelines),
            sorted(self.pipelines),
        )
