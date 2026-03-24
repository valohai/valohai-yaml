from collections.abc import Iterator
from typing import Union

import jsonschema

ErrorType = Union[str, jsonschema.ValidationError]


class InvalidType(TypeError):
    """A type error specific to valohai-yaml."""


class ValidationError(ValueError):
    """Generic validation error."""


class ValidationErrors(ValidationError):
    """Wrapper for multiple validation errors."""

    def __init__(self, errors: list[ErrorType]) -> None:
        self.errors = errors
        err_desc = ", ".join(getattr(e, "message", e) for e in self.errors)
        super().__init__(f"{len(errors)} errors: {err_desc}")

    def __iter__(self) -> Iterator[ErrorType]:
        """Iterate over the errors contained within."""
        return iter(self.errors)
