from __future__ import annotations

from enum import Enum
from typing import Any

from valohai_yaml.lint import LintResult
from valohai_yaml.objs.base import Item
from valohai_yaml.objs.utils import (
    check_type_and_listify,
    consume_array_of,
)
from valohai_yaml.objs.variant_parameter import VariantParameter
from valohai_yaml.types import LintContext
from valohai_yaml.utils.lint import lint_expression

# Properties that only make sense for Bayesian tasks.
BAYESIAN_ONLY_PROPS = (
    "engine",
    "optimization_target_metric",
    "optimization_target_value",
)


class TaskType(Enum):
    """Represents a task type."""

    BAYESIAN_TPE = "bayesian_tpe"
    GRID_SEARCH = "grid_search"
    DISTRIBUTED = "distributed"
    RANDOM_SEARCH = "random_search"
    MANUAL_SEARCH = "manual_search"

    @classmethod
    def cast(cls, value: TaskType | str | None) -> TaskType:
        if not value:
            return TaskType.GRID_SEARCH
        if isinstance(value, TaskType):
            return value
        value = str(value).lower().replace("-", "_")
        return TaskType(value)


class TaskOnChildError(Enum):
    """Represents the possible actions that can be taken when a task's child fails."""

    CONTINUE_AND_COMPLETE = "continue-and-complete"
    CONTINUE_AND_ERROR = "continue-and-error"
    STOP_ALL_AND_ERROR = "stop-all-and-error"

    @classmethod
    def cast(cls, value: TaskOnChildError | str | None) -> TaskOnChildError | None:
        if not value:
            return None
        if isinstance(value, TaskOnChildError):
            return value
        value = str(value).lower().replace("_", "-")
        return TaskOnChildError(value)


class Task(Item):
    """Represents a task definition."""

    step: str
    type: TaskType
    parameters: list[VariantParameter]
    parameter_sets: list[dict[str, Any]]
    name: str
    execution_count: int | None
    execution_batch_size: int | None
    maximum_queued_executions: int | None
    optimization_target_metric: str | None
    optimization_target_value: float | None
    engine: str | None
    on_child_error: TaskOnChildError | None

    def __init__(
        self,
        *,
        name: str,
        step: str,
        type: TaskType | str | None = None,
        parameters: list[VariantParameter] | None = None,
        parameter_sets: list[dict[str, Any]] | None = None,
        execution_count: int | None = None,
        execution_batch_size: int | None = None,
        maximum_queued_executions: int | None = None,
        optimization_target_metric: str | None = None,
        optimization_target_value: float | None = None,
        engine: str | None = None,
        on_child_error: TaskOnChildError | None = None,
        stop_condition: str | None = None,
    ) -> None:
        self.name = name
        self.step = step
        self.type = TaskType.cast(type)
        self.parameters = check_type_and_listify(parameters, VariantParameter)
        self.parameter_sets = [
            ps for ps in check_type_and_listify(parameter_sets, dict) if ps
        ]
        self.execution_count = execution_count
        self.execution_batch_size = execution_batch_size
        self.maximum_queued_executions = maximum_queued_executions
        self.optimization_target_metric = optimization_target_metric
        self.optimization_target_value = optimization_target_value
        self.engine = engine
        self.on_child_error = TaskOnChildError.cast(on_child_error)
        self.stop_condition = stop_condition

    @classmethod
    def parse(cls, data: Any) -> Task:
        kwargs = data.copy()
        kwargs["parameters"] = consume_array_of(kwargs, "parameters", VariantParameter)
        inst = cls(**{key.replace("-", "_"): value for key, value in kwargs.items()})
        inst._original_data = data
        return inst

    def lint(self, lint_result: LintResult, context: LintContext) -> None:
        context = dict(context, task=self, object_type="task")
        lint_expression(lint_result, context, "stop-condition", self.stop_condition)
        if self.parameter_sets and self.type != TaskType.MANUAL_SEARCH:
            lint_result.add_warning("Parameter sets only make sense with manual search")
        if self.type != TaskType.BAYESIAN_TPE:
            for key in BAYESIAN_ONLY_PROPS:
                if getattr(self, key) is not None:
                    lint_result.add_warning(
                        f"{key} only makes sense for Bayesian TPE tasks",
                    )
