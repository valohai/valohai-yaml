# Via Click.
#     Click is:
#     :copyright: (c) 2014 by Armin Ronacher.
#     :license: BSD, see LICENSE for more details.

from typing import Any, Optional

_ansi_colors = (
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "reset",
)

_ansi_reset_all = "\033[0m"


def style(  # noqa: C901
    text: str,
    *,
    fg: Optional[str] = None,
    bg: Optional[str] = None,
    bold: Optional[bool] = None,
    dim: Optional[bool] = None,
    underline: Optional[bool] = None,
    blink: Optional[bool] = None,
    reverse: Optional[bool] = None,
    reset: bool = True,
) -> str:
    """Styles a text with ANSI styles and returns the new string."""
    bits = []
    if fg:
        try:
            bits.append("\033[%dm" % (_ansi_colors.index(fg) + 30))
        except ValueError as err:
            raise TypeError(f"Unknown color {fg!r}") from err
    if bg:
        try:
            bits.append("\033[%dm" % (_ansi_colors.index(bg) + 40))
        except ValueError as err:
            raise TypeError(f"Unknown color {bg!r}") from err
    if bold is not None:
        bits.append("\033[%dm" % (1 if bold else 22))
    if dim is not None:
        bits.append("\033[%dm" % (2 if dim else 22))
    if underline is not None:
        bits.append("\033[%dm" % (4 if underline else 24))
    if blink is not None:
        bits.append("\033[%dm" % (5 if blink else 25))
    if reverse is not None:
        bits.append("\033[%dm" % (7 if reverse else 27))
    bits.append(text)
    if reset:
        bits.append(_ansi_reset_all)
    return "".join(bits)


def noop_style(text: str, **kwargs: Any) -> str:
    """Return the original text, unstyled."""
    return text
