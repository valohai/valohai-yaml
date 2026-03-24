from __future__ import annotations

from typing import TYPE_CHECKING, Any

from leval.rewriter_evaluator import RewriterEvaluator
from leval.universe.verifier import VerifierUniverse

if TYPE_CHECKING:
    from collections.abc import Iterable

    from valohai_yaml.lint import LintResult
    from valohai_yaml.types import LintContext


class _KeywordRewriterEvaluator(RewriterEvaluator):
    def rewrite_keyword(self, kw: str) -> str:
        return f"_{kw}"


def lint_iterables(
    lint_result: LintResult,
    context: LintContext,
    iterables: Iterable[Iterable[Any]],
) -> None:
    for iterable in iterables:
        if isinstance(iterable, dict):
            iterable = iterable.values()
        for item in iterable:
            if hasattr(item, "lint"):
                item.lint(lint_result, context)


def lint_expression(
    lint_result: LintResult,
    context: LintContext,
    field_name: str,
    expression: str | None,
) -> None:
    if expression is None:
        return

    universe = VerifierUniverse()
    evl = _KeywordRewriterEvaluator(universe, max_depth=8)
    object_type = context["object_type"]
    try:
        evl.evaluate_expression(expression)
    except Exception as e:
        lint_result.add_error(
            f"{object_type.capitalize()} {context[object_type].name}, `{field_name}` is not a valid expression: {e}",
        )
