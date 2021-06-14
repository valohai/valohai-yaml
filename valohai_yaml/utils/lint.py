from typing import Any, Dict, Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from valohai_yaml.lint import LintResult


def lint_iterables(lint_result: 'LintResult', context: Dict[str, Any], iterables: Iterable[Iterable[Any]]) -> None:
    for iterable in iterables:
        if isinstance(iterable, dict):
            iterable = iterable.values()
        for item in iterable:
            if hasattr(item, 'lint'):
                item.lint(lint_result, context)
