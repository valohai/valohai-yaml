from typing import Optional

from valohai_yaml.excs import LevalNotAvailable
from valohai_yaml.lint import LintResult
from valohai_yaml.types import LintContext


def lint_expression(
    lint_result: "LintResult",
    context: LintContext,
    field_name: str,
    expression: Optional[str],
) -> None:
    if expression is None:
        return

    try:
        from leval.rewriter_evaluator import RewriterEvaluator
        from leval.universe.verifier import VerifierUniverse
    except ImportError as e:
        raise LevalNotAvailable("Leval is not available, can't lint expression") from e

    class _KeywordRewriterEvaluator(RewriterEvaluator):
        def rewrite_keyword(self, kw: str) -> str:
            return f"_{kw}"

    universe = VerifierUniverse()
    evl = _KeywordRewriterEvaluator(universe, max_depth=8)
    object_type = context["object_type"]
    try:
        evl.evaluate_expression(expression)
    except Exception as e:
        lint_result.add_error(
            f"{object_type.capitalize()} {context[object_type].name}, "
            f"`{field_name}` is not a valid expression: {e}",
        )
