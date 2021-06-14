from typing import List, Union

import jsonschema


class ValidationError(ValueError):
    """Generic validation error."""


class ValidationErrors(ValidationError):
    """Wrapper for multiple validation errors."""

    def __init__(self, errors: List[Union[str, jsonschema.ValidationError]]) -> None:
        self.errors = errors
        super().__init__(
            '%d errors: %s' % (
                len(errors),
                ', '.join(getattr(e, 'message', e) for e in self.errors)
            )
        )

    def __iter__(self):  # noqa: ANN204
        """Iterate over the errors contained within."""
        return iter(self.errors)
