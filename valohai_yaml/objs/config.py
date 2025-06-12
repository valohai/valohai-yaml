import copy
from itertools import chain
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

from valohai_yaml.excs import InvalidType
from valohai_yaml.lint import LintResult
from valohai_yaml.objs.base import Item
from valohai_yaml.objs.endpoint import Endpoint
from valohai_yaml.objs.pipelines.pipeline import Pipeline
from valohai_yaml.objs.step import Step
from valohai_yaml.objs.task import Task
from valohai_yaml.objs.utils import check_type_and_dictify
from valohai_yaml.types import LintContext, SerializedDict
from valohai_yaml.utils.lint import lint_iterables
from valohai_yaml.utils.merge import merge_dicts, merge_simple

ParserFunction = Callable[[SerializedDict], Any]


class Config(Item):
    """Represents a `valohai.yaml` file."""

    # Warnings that may be stuck on the top-level config during its parsing.
    _parse_warnings = None

    def __init__(
        self,
        *,
        steps: Iterable[Step] = (),
        tasks: Iterable[Task] = (),
        endpoints: Iterable[Endpoint] = (),
        pipelines: Iterable[Pipeline] = (),
    ) -> None:
        self.steps = check_type_and_dictify(steps, Step, "name")
        self.tasks = check_type_and_dictify(tasks, Task, "name")
        self.endpoints = check_type_and_dictify(endpoints, Endpoint, "name")
        self.pipelines = check_type_and_dictify(pipelines, Pipeline, "name")

    @classmethod
    def parse(cls, data: Iterable) -> "Config":
        """
        Parse a Config structure out of a list of Python dicts (that's likely deserialized from YAML).

        :param data: Config-y iterable container of dicts
        :return: Config object
        """
        parsers = cls.get_top_level_parsers()
        parse_warnings: List[str] = []
        append_warning_if_not_unique = _get_unique_name_checker(parse_warnings)

        for datum in data:
            if not isinstance(datum, dict):
                raise InvalidType(f"Top-level YAML item {datum} is not a dictionary")
            for item_type, (items, parse) in parsers.items():
                if item_type in datum:
                    items.append(parsed_item := parse(datum[item_type]))
                    append_warning_if_not_unique(item_type, parsed_item)
                    break
            else:
                parse_warnings.append(f"No parser for {datum}")

        inst = cls(
            steps=parsers["step"][0],
            endpoints=parsers["endpoint"][0],
            pipelines=parsers["pipeline"][0],
            tasks=parsers["task"][0],
        )
        inst._original_data = data
        inst._parse_warnings = parse_warnings
        return inst

    @classmethod
    def get_top_level_parsers(cls) -> Dict[str, Tuple[List[Any], ParserFunction]]:
        """
        Get the parsers for top-level elements in a configuration file.

        The return value is a little baroque due to the alias for `pipeline`/`blueprint`:
        it's a dict that maps top-level element names to a 2-tuple of target list objects and parse functions.
        """
        pipelines: List[Pipeline] = []
        return {
            "step": ([], Step.parse),
            "task": ([], Task.parse),
            "endpoint": ([], Endpoint.parse),
            "pipeline": (pipelines, Pipeline.parse),
            "blueprint": (pipelines, Pipeline.parse),  # Alias allowed for now
        }

    def serialize(self) -> List[SerializedDict]:
        return list(
            chain(
                ({"step": step.serialize()} for (key, step) in self.steps.items()),
                ({"task": task.serialize()} for (key, task) in self.tasks.items()),
                ({"endpoint": endpoint.serialize()} for (key, endpoint) in sorted(self.endpoints.items())),
                ({"pipeline": pipeline.serialize()} for (key, pipeline) in sorted(self.pipelines.items())),
            ),
        )

    def lint(  # type: ignore[override]
        self,
        lint_result: Optional[LintResult] = None,
        context: Optional[LintContext] = None,
    ) -> LintResult:
        """
        Lint the configuration.

        :param lint_result: LintResult object. Optional; if not passed in, one is constructed.
        :param context: Optional context dictionary; should likely not be passed in at top level.
        :return: The lint result object used.
        """
        if context is None:
            context = {}
        if lint_result is None:
            lint_result = LintResult()
        context = dict(context, config=self)

        if self._parse_warnings:
            for warning in self._parse_warnings:
                lint_result.add_warning(warning)

        lint_iterables(
            lint_result,
            context,
            (
                self.steps,
                self.endpoints,
                self.pipelines,
                self.tasks,
            ),
        )
        return lint_result

    def get_step_by(self, **kwargs: Any) -> Optional[Step]:
        """
        Get the first step that matches all the passed named arguments.

        Has special argument index not present in the real step.

        Usage:
            config.get_step_by(name='not found')
            config.get_step_by(index=0)
            config.get_step_by(name="greeting", command='echo HELLO MORDOR')

        :param kwargs:
        :return: Step object or None
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
    def default_merge(cls, a: "Config", b: "Config") -> "Config":
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

    def __repr__(self) -> str:  # pragma: no cover  # noqa: D105
        return (
            f"<Config with {len(self.steps)} steps ({self.steps!r}), "
            f"{len(self.endpoints)} endpoints ({sorted(self.endpoints)!r}), "
            f"and {len(self.pipelines)} pipelines ({sorted(self.pipelines)!r})>"
        )


def _get_unique_name_checker(parse_warnings: List[str]) -> Callable:
    """
    Return a unique name checker function that records if there is a name clash in the config.

    Checks within the item type, i.e., two steps with the same name is a warning,
    but not a step and a task with the same name. Adds the warnings to parse_warnings.
    """
    used_item_names = set()

    def checker(item_type: str, item: Any) -> None:
        try:
            if (item_type, item.name) in used_item_names:
                parse_warnings.append(f"Duplicate {item_type} name: {item.name}.")
            used_item_names.add((item_type, item.name))
        except AttributeError:
            # all current items have a name, but that is not guaranteed for the future
            # so make sure things don't break if we get a top-level item without a name
            pass

    return checker
