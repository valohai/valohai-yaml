import six

from valohai_yaml.validation import ValidationErrors
from .base import _SimpleObject


class Parameter(_SimpleObject):
    def __init__(
        self,
        name,
        type='string',
        optional=False,
        min=None,
        max=None,
        description=None,
        default=None,
        pass_as=None,
        choices=None,
    ):
        self.name = name
        self.type = type
        self.optional = bool(optional)
        self.min = min
        self.max = max
        self.description = description
        self.default = default
        self.pass_as = pass_as
        self.choices = (list(choices) if choices else None)

    def _validate_value(self, value, errors):
        if self.min is not None and value < self.min:
            errors.append('%s is less than the minimum allowed (%s)' % (value, self.min))
        if self.max is not None and value > self.max:
            errors.append('%s is greater than the maximum allowed (%s)' % (value, self.max))
        if self.choices is not None and value not in self.choices:
            errors.append('%s is not among the choices allowed (%r)' % (value, self.choices))

    def _validate_type(self, value, errors):
        if self.type == 'integer':
            try:
                value = int(six.text_type(value), 10)
            except ValueError:
                errors.append('%s is not an integer' % value)
        elif self.type == 'float':
            try:
                value = float(six.text_type(value))
            except ValueError:
                errors.append('%s is not a floating-point number' % value)
        return value

    def validate(self, value):
        """
        Validate (and possibly typecast) the given parameter value value.

        :param value: Parameter value
        :return: Typecast parameter value
        :raises ValidationErrors: if there were validation errors
        """
        errors = []
        value = self._validate_type(value, errors)
        self._validate_value(value, errors)

        if errors:
            raise ValidationErrors(errors)

        return value
