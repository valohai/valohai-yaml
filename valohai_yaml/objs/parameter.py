from enum import Enum
from typing import Any, Iterable, List, Optional, Union

from valohai_yaml.excs import InvalidType, ValidationErrors
from valohai_yaml.lint import LintResult
from valohai_yaml.objs.base import Item
from valohai_yaml.objs.parameter_widget import ParameterWidget
from valohai_yaml.types import LintContext, SerializedDict
from valohai_yaml.utils import listify


class MultipleMode(Enum):
    """How to serialize multiple values given for a parameter."""

    SEPARATE = "separate"
    REPEAT = "repeat"

    @classmethod
    def cast(
        cls,
        value: Optional[Union["MultipleMode", str]],
    ) -> Optional["MultipleMode"]:
        if not value:
            return None
        if isinstance(value, MultipleMode):
            return value
        value = str(value).lower()
        if value == "none":
            return None
        return MultipleMode(value)


ValueAtomType = Union[float, str, int, bool]
ValueType = Union[List[ValueAtomType], ValueAtomType]


class Parameter(Item):
    """Represents a parameter definition within an execution step definition."""

    def __init__(
        self,
        *,
        name: str,
        type: str = "string",
        optional: bool = False,
        min: Optional[ValueAtomType] = None,
        max: Optional[ValueAtomType] = None,
        description: Optional[str] = None,
        default: Optional[Any] = None,
        pass_as: Optional[str] = None,
        pass_true_as: Optional[str] = None,
        pass_false_as: Optional[str] = None,
        choices: Optional[Iterable[ValueAtomType]] = None,
        multiple: Optional[Union[str, MultipleMode]] = None,
        multiple_separator: str = ",",
        widget: Optional[ParameterWidget] = None,
    ) -> None:
        self.name = name
        self.type = type
        self.optional = bool(optional)
        self.min = min
        self.max = max
        self.description = description
        self.pass_as = pass_as
        self.pass_true_as = pass_true_as
        self.pass_false_as = pass_false_as
        self.choices = list(choices) if choices else None
        self.multiple = MultipleMode.cast(multiple)
        self.multiple_separator = str(multiple_separator or ",")
        self.widget = widget

        self.default = listify(default) if self.multiple else default
        if self.type == "flag":
            self.optional = True
            self.choices = [True, False]
            if self.multiple:
                raise ValueError("Flag parameters can't be multiple")
        else:
            self.pass_true_as = self.pass_false_as = None

    def get_data(self) -> SerializedDict:
        data = super().get_data()
        if self.type == "flag":
            data.pop("optional", None)
            data.pop("choices", None)
        if self.multiple:
            data["multiple"] = data["multiple"].value
        else:
            data.pop("multiple_separator", None)
        return data

    def _validate_value(self, value: ValueAtomType, errors: List[str]) -> ValueAtomType:
        try:
            if self.min is not None and value < self.min:  # type: ignore
                errors.append(f"{value} is less than the minimum allowed ({self.min})")
        except TypeError:  # Could occur if types are incompatible
            pass
        try:
            if self.max is not None and value > self.max:  # type: ignore
                errors.append(
                    f"{value} is greater than the maximum allowed ({self.max})",
                )
        except TypeError:
            pass
        if self.choices is not None and value not in self.choices:
            errors.append(
                f"{value} is not among the choices allowed ({self.choices!r})",
            )
        return value

    def _validate_type(self, value: ValueAtomType, errors: List[str]) -> ValueAtomType:
        if self.type == "integer":
            try:
                value = int(str(value), 10)
            except ValueError:
                if value == "":
                    errors.append("No value supplied")
                else:
                    errors.append(f"{value} is not an integer")
        elif self.type == "float":
            try:
                value = float(str(value))
            except ValueError:
                if value == "":
                    errors.append("No value supplied")
                else:
                    errors.append(f"{value} is not a floating-point number")
        return value

    def validate(self, value: ValueType) -> ValueType:
        """
        Validate (and possibly typecast) the given parameter value.

        :param value: Parameter value
        :return: Typecast parameter value
        :raises ValidationErrors: if there were validation errors
        """
        errors = []
        validated_values = []

        if not self.multiple and isinstance(value, (list, tuple)):
            errors.append("Only a single value is allowed")

        if value is None:
            errors.append("No value supplied")

        for atom in listify(value):
            if isinstance(atom, list):  # type guard
                raise InvalidType(f"nested list atom {atom!r} not allowed")
            atom = self._validate_type(atom, errors)
            atom = self._validate_value(atom, errors)
            validated_values.append(atom)

        if errors:
            raise ValidationErrors(errors)

        if self.multiple:
            return validated_values
        return validated_values[0]

    @property
    def default_pass_as(self) -> str:
        if self.type == "flag":
            return "--{name}"
        return "--{name}={value}"

    def _get_pass_as_template(self, value: Optional[ValueType]) -> Optional[str]:
        if self.type == "flag":
            if self.pass_true_as or self.pass_false_as:
                return (self.pass_true_as if value else self.pass_false_as) or None
            if not value:
                return None

        if value is None:
            return None

        return str(self.pass_as or self.default_pass_as)

    def format_cli(self, value: Optional[ValueType]) -> Optional[List[str]]:
        """
        Build a parameter argument (or multiple, if this is a multi-valued parameter).

        :return: list of CLI strings -- not escaped. If the parameter should not be expressed, returns None.
        """
        pass_as_template = self._get_pass_as_template(value)
        if not pass_as_template:
            return None

        pass_as_bits = pass_as_template.split()

        def _format_atom(value: Optional[ValueAtomType]) -> List[str]:
            env = {"name": self.name, "value": value, "v": value}
            return [bit.format_map(env) for bit in pass_as_bits]

        if self.multiple == MultipleMode.REPEAT:
            out = []
            for atom in listify(value):
                if isinstance(atom, list):
                    raise InvalidType(
                        f"nested list value {atom!r} for repeat-style multiple parameter not allowed",
                    )
                out.extend(_format_atom(atom))
            return out

        if self.multiple == MultipleMode.SEPARATE:
            value_list = listify(value)
            # Guard against generating a `--foo=` when there are no values.
            if value_list:
                return _format_atom(
                    self.multiple_separator.join(str(atom) for atom in value_list),
                )
            return None

        if not self.multiple:
            if isinstance(value, list):
                raise InvalidType(
                    f"list value {value!r} for non-multiple parameter {self.name!r} not allowed",
                )
            return _format_atom(value)

        raise NotImplementedError(f"unknown multiple type {self.multiple!r}")

    @classmethod
    def parse(cls, data: SerializedDict) -> "Parameter":
        kwargs = data.copy()
        if "widget" in data:
            kwargs["widget"] = ParameterWidget.parse(data["widget"])
        return super().parse(kwargs)

    def lint(
        self,
        lint_result: LintResult,
        context: LintContext,
    ) -> None:
        original_data = self._original_data or {}
        has_pass_as = bool(original_data.get("pass-as"))
        has_pass_true_as = bool(original_data.get("pass-true-as"))
        has_pass_false_as = bool(original_data.get("pass-false-as"))
        prefix = f'Step {context["step"].name}, parameter {self.name}'
        if self.type == "flag":
            if original_data.get("optional"):
                lint_result.add_warning(
                    f"{prefix}: `optional` has no effect on flag-type parameters",
                )
            if (has_pass_true_as or has_pass_false_as) and has_pass_as:
                lint_result.add_warning(
                    f"{prefix}: `pass-as` has no effect with `pass-true-as`/`pass-false-as`",
                )
        else:
            if has_pass_true_as:
                lint_result.add_warning(
                    f"{prefix}: `pass-true-as` has no effect on non-flag parameters",
                )
            if has_pass_false_as:
                lint_result.add_warning(
                    f"{prefix}: `pass-false-as` has no effect on non-flag parameters",
                )

        if self.default:
            errors = []
            for default_value in listify(self.default):
                if self.type == "string" and not isinstance(default_value, str):
                    errors.append(
                        f"`default` value {default_value!r} is not a string (got a {type(default_value)})",
                    )
                else:
                    self._validate_type(default_value, errors)
                    self._validate_value(default_value, errors)

            for message in errors:
                lint_result.add_warning(f"{prefix}: default {message}")
