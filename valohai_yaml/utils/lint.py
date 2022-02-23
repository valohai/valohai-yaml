from typing import TYPE_CHECKING, Any, Iterable

from valohai_yaml.types import LintContext

if TYPE_CHECKING:
    from valohai_yaml.lint import LintResult


def lint_iterables(
    lint_result: 'LintResult',
    context: LintContext,
    iterables: Iterable[Iterable[Any]],
) -> None:
    for iterable in iterables:
        if isinstance(iterable, dict):
            iterable = iterable.values()
        for item in iterable:
            if hasattr(item, 'lint'):
                item.lint(lint_result, context)
