from typing import Optional

from valohai_yaml.lint import LintResult
from valohai_yaml.objs.base import Item
from valohai_yaml.types import DeploymentDefaultsDict, LintContext


class Deployment(Item):
    """Represents a deployment in a project under where deployment versions and endpoints are housed."""

    def __init__(
        self,
        *,
        name: str,
        defaults: Optional[DeploymentDefaultsDict] = None,
    ) -> None:
        self.name = name
        self.defaults = defaults

    def lint(self, lint_result: LintResult, context: LintContext) -> None:
        super().lint(lint_result, context)
        default_target = self.defaults.get("target") if self.defaults else None
        if not default_target:
            lint_result.add_warning(
                f'Deployment "{self.name}" has no defaults.target set which is required for deployment auto-creation.',
            )
            return
