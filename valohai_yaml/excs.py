from typing import List, Union

import jsonschema


class ValidationError(ValueError):
    pass


class ValidationErrors(ValidationError):

    def __init__(self, errors: List[Union[str, jsonschema.ValidationError]]) -> None:
        self.errors = errors
        super(ValidationErrors, self).__init__(
            '%d errors: %s' % (
                len(errors),
                ', '.join(getattr(e, 'message', e) for e in self.errors)
            )
        )

    def __iter__(self):
        return iter(self.errors)
