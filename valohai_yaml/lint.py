from typing import Any, Callable, Iterator, List, Optional

import yaml as pyyaml
from jsonschema.exceptions import relevance

from valohai_yaml.excs import ValidationError
from valohai_yaml.types import LintResultMessage, YamlReadable
from valohai_yaml.utils import read_yaml
from valohai_yaml.utils.terminal import noop_style, style
from valohai_yaml.validation import get_validator


class LintResult:
    """Container for lint results."""

    def __init__(self) -> None:
        self.messages: List[LintResultMessage] = []

    def add_error(
        self,
        message: str,
        location: None = None,
        exception: Optional[Exception] = None,
    ) -> None:
        self.messages.append(
            {
                "type": "error",
                "message": message,
                "location": location,
                "exception": exception,
            },
        )

    def add_warning(
        self,
        message: str,
        location: None = None,
        exception: Optional[Exception] = None,
    ) -> None:
        self.messages.append(
            {
                "type": "warning",
                "message": message,
                "location": location,
                "exception": exception,
            },
        )

    def add_hint(
        self,
        message: str,
        location: None = None,
        exception: Optional[Exception] = None,
    ) -> None:
        self.messages.append(
            {
                "type": "hint",
                "message": message,
                "location": location,
                "exception": exception,
            },
        )

    @property
    def warning_count(self) -> int:
        return sum(1 for m in self.messages if m["type"] == "warning")

    @property
    def error_count(self) -> int:
        return sum(1 for m in self.messages if m["type"] == "error")

    @property
    def warnings(self) -> Iterator[LintResultMessage]:
        return (m for m in self.messages if m["type"] == "warning")

    @property
    def errors(self) -> Iterator[LintResultMessage]:
        return (m for m in self.messages if m["type"] == "error")

    @property
    def hints(self) -> Iterator[LintResultMessage]:
        return (m for m in self.messages if m["type"] == "hint")

    def is_valid(self) -> bool:
        return self.warning_count == 0 and self.error_count == 0


def lint_file(file_path: str, *, validate_schema: bool = True) -> LintResult:
    """
    Validate & lint `file_path` and return a LintResult.

    :param file_path: YAML filename
    :param validate_schema: Whether to validate against the JSON schema before attempting to parse and lint.
                            This should generally always be true, but can be disabled for testing purposes.
    :return: LintResult object
    """
    with open(file_path) as yaml:
        try:
            return lint(yaml, validate_schema=validate_schema)
        except Exception as e:
            lr = LintResult()
            lr.add_error(f"could not parse YAML: {e}", exception=e)
            return lr


def _validate_json_schema(
    lr: LintResult,
    data: Any,
    styler: Callable[..., str] = style,
) -> int:
    """Validate against the JSON schema; add errors to `lr` and return the number of errors."""
    errors = sorted(
        get_validator().iter_errors(data),
        key=lambda error: (relevance(error), repr(error.path)),
    )
    for error in errors:
        simplified_schema_path = [
            el
            for el in list(error.relative_schema_path)
            if el not in ("properties", "items")
        ]
        obj_path = [str(el) for el in error.path]
        styled_validator = styler(error.validator.title(), bold=True)
        styled_schema_path = styler(".".join(simplified_schema_path), bold=True)
        styled_message = styler(error.message, fg="red")
        styled_path = styler(".".join(obj_path), bold=True)
        lr.add_error(
            f"  {styled_validator} validation on {styled_schema_path}: {styled_message} ({styled_path})",
        )
        # when path has only 2 nodes. it means it has problem in main steps/pipelines/endpoints objects
        if len(error.path) == 2 and not error.instance:
            styled_hint = styler(
                "File contains valid YAML but there might be an indentation "
                f"error in following configuration: {styled_path}",
                fg="blue",
            )
            lr.add_hint(styled_hint)
    return len(errors)


def lint(
    yaml: YamlReadable,
    *,
    validate_schema: bool = True,
    ansi_colors: bool = True,
) -> LintResult:
    """
    Validate & lint `yaml` and return a `LintResult`.

    :param yaml: YAML string or file-like object
    :param validate_schema: Whether to validate against the JSON schema before attempting to parse and lint.
                            This should generally always be true, but can be disabled for testing purposes.
    :param ansi_colors: Whether to use ANSI colors in the output.
    """
    lr = LintResult()
    try:
        data = read_yaml(yaml)
    except pyyaml.YAMLError as err:
        if hasattr(err, "problem_mark"):
            mark = err.problem_mark
            indent_error = (
                f"Indentation Error at line {mark.line + 1}, column {mark.column + 1}"
            )
            lr.add_error(indent_error)
        else:
            lr.add_error(str(err))
        return lr

    if validate_schema and _validate_json_schema(
        lr,
        data,
        styler=style if ansi_colors else noop_style,  # type: ignore[arg-type]
    ):
        # If validation found errors, don't try to parse the data
        return lr

    try:
        from valohai_yaml.objs import Config

        config = Config.parse(data)
    except ValidationError as err:  # Could happen before we get to linting things
        lr.add_error(str(err), exception=err)
    else:
        config.lint(lr, context={})
    return lr
