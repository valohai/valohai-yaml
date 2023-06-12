from __future__ import annotations

from enum import Enum
from typing import Any

from valohai_yaml.objs.base import Item
from valohai_yaml.objs.utils import (
    check_type_and_listify,
    consume_array_of,
)
from valohai_yaml.objs.variant_parameter import VariantParameter


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
        value = str(value).lower()
        return TaskType(value)


class Task(Item):
    """Represents a task definition."""

    step: str
    type: TaskType
    parameters: list[VariantParameter]
    name: str
    execution_count: int | None
    execution_batch_size: int | None
    optimization_target_metric: str | None
    optimization_target_value: float | None
    engine: str | None

    def __init__(
        self,
        *,
        name: str,
        step: str,
        type: TaskType | str | None = None,
        parameters: list[VariantParameter] | None = None,
        execution_count: int | None = None,
        execution_batch_size: int | None = None,
        optimization_target_metric: str | None = None,
        optimization_target_value: float | None = None,
        engine: str | None = None,
    ) -> None:
        self.name = name
        self.step = step
        self.type = TaskType.cast(type)
        self.parameters = check_type_and_listify(parameters, VariantParameter)
        self.execution_count = execution_count
        self.execution_batch_size = execution_batch_size
        self.optimization_target_metric = optimization_target_metric
        self.optimization_target_value = optimization_target_value
        self.engine = engine

    @classmethod
    def parse(cls, data: Any) -> Task:
        kwargs = data.copy()
        kwargs["parameters"] = consume_array_of(kwargs, "parameters", VariantParameter)
        inst = cls(**kwargs)
        inst._original_data = data
        return inst
