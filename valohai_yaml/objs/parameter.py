from enum import Enum
from typing import List, Optional, Union

from valohai_yaml.utils import listify
from valohai_yaml.validation import ValidationErrors
from .base import Item


class MultipleMode(Enum):
    SEPARATE = 'separate'
    REPEAT = 'repeat'

    @classmethod
    def cast(cls, value):
        if not value:
            return None
        value = str(value).lower()
        if value == 'none':
            return None
        return MultipleMode(value)


ValueAtomType = Union[float, str, int, bool]
ValueType = Union[List[ValueAtomType], ValueAtomType]


class Parameter(Item):

    def __init__(
        self,
        *,
        name,
        type='string',
        optional=False,
        min=None,
        max=None,
        description=None,
        default=None,
        pass_as=None,
        pass_true_as=None,
        pass_false_as=None,
        choices=None,
        multiple=None,
        multiple_separator=','
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
        self.choices = (list(choices) if choices else None)
        self.multiple = MultipleMode.cast(multiple)
        self.multiple_separator = str(multiple_separator or ',')
        self.default = (listify(default) if self.multiple else default)
        if self.type == 'flag':
            self.optional = True
            self.choices = (True, False)
            if self.multiple:
                raise ValueError('Flag parameters can\'t be multiple')
        else:
            self.pass_true_as = self.pass_false_as = None

    def get_data(self) -> dict:
        data = super(Parameter, self).get_data()
        if self.type == 'flag':
            data.pop('optional', None)
            data.pop('choices', None)
        if self.multiple:
            data['multiple'] = data['multiple'].value
        else:
            data.pop('multiple-separator', None)
        return data

    def _validate_value(self, value: ValueAtomType, errors: List[str]) -> ValueAtomType:
        try:
            if self.min is not None and value < self.min:
                errors.append('%s is less than the minimum allowed (%s)' % (value, self.min))
        except TypeError:  # Could occur if types are incompatible
            pass
        try:
            if self.max is not None and value > self.max:
                errors.append('%s is greater than the maximum allowed (%s)' % (value, self.max))
        except TypeError:
            pass
        if self.choices is not None and value not in self.choices:
            errors.append('%s is not among the choices allowed (%r)' % (value, self.choices))
        return value

    def _validate_type(self, value: ValueAtomType, errors: list) -> ValueAtomType:
        if self.type == 'integer':
            try:
                value = int(str(value), 10)
            except ValueError:
                errors.append('%s is not an integer' % value)
        elif self.type == 'float':
            try:
                value = float(str(value))
            except ValueError:
                errors.append('%s is not a floating-point number' % value)
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
            errors.append('Only a single value is allowed')

        for atom in listify(value):
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
        if self.type == 'flag':
            return '--{name}'
        return '--{name}={value}'

    def _get_pass_as_template(self, value: Optional[ValueType]) -> Optional[str]:
        if self.type == 'flag':
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
        :rtype: list[str]|None
        """
        pass_as_template = self._get_pass_as_template(value)
        if not pass_as_template:
            return None

        pass_as_bits = pass_as_template.split()

        def _format_atom(value: ValueAtomType) -> List[str]:
            env = dict(name=self.name, value=value, v=value)
            return [bit.format(**env) for bit in pass_as_bits]

        if self.multiple == MultipleMode.REPEAT:
            out = []
            for atom in listify(value):
                out.extend(_format_atom(atom))
            return out
        elif self.multiple == MultipleMode.SEPARATE:
            value_list = listify(value)
            # Guard against generating a `--foo=` when there are no values.
            if value_list:
                return _format_atom(self.multiple_separator.join(str(atom) for atom in value_list))
            return None
        elif not self.multiple:
            return _format_atom(value)
        else:
            raise NotImplementedError('unknown multiple type %r' % self.multiple)

    def lint(
        self,
        lint_result,
        context: dict
    ) -> None:
        has_pass_as = bool(self._original_data.get('pass-as'))
        has_pass_true_as = bool(self._original_data.get('pass-true-as'))
        has_pass_false_as = bool(self._original_data.get('pass-false-as'))
        context_prefix = 'Step {step}, parameter {param}'.format(
            step=context['step'].name,
            param=self.name,
        )
        if self.type == 'flag':
            if self._original_data.get('optional'):
                lint_result.add_warning('{prefix}: `optional` has no effect on flag-type parameters'.format(
                    prefix=context_prefix,
                ))
            if (has_pass_true_as or has_pass_false_as) and has_pass_as:
                lint_result.add_warning('{prefix}: `pass-as` has no effect with `pass-true-as`/`pass-false-as`'.format(
                    prefix=context_prefix,
                ))
        else:
            if has_pass_true_as:
                lint_result.add_warning('{prefix}: `pass-true-as` has no effect on non-flag parameters'.format(
                    prefix=context_prefix,
                ))
            if has_pass_false_as:
                lint_result.add_warning('{prefix}: `pass-false-as` has no effect on non-flag parameters'.format(
                    prefix=context_prefix,
                ))

        if self.default:
            errors = []
            for default_value in listify(self.default):
                if self.type == 'string' and not isinstance(default_value, str):
                    errors.append(
                        '`default` value {value!r} is not a string (got a {type})'.format(
                            value=default_value,
                            type=type(default_value),
                        ))
                else:
                    self._validate_type(default_value, errors)
                    self._validate_value(default_value, errors)

            for message in errors:
                lint_result.add_warning('{prefix}: default {message}'.format(prefix=context_prefix, message=message))
