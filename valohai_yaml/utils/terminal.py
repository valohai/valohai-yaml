# Via Click.
#     Click is:
#     :copyright: (c) 2014 by Armin Ronacher.
#     :license: BSD, see LICENSE for more details.

_ansi_colors = ('black', 'red', 'green', 'yellow', 'blue', 'magenta',
                'cyan', 'white', 'reset')
_ansi_reset_all = '\033[0m'


def style(text, fg=None, bg=None, bold=None, dim=None, underline=None,  # noqa: C901
          blink=None, reverse=None, reset=True):
    """Styles a text with ANSI styles and returns the new string."""
    bits = []
    if fg:
        try:
            bits.append('\033[%dm' % (_ansi_colors.index(fg) + 30))
        except ValueError:
            raise TypeError('Unknown color %r' % fg)
    if bg:
        try:
            bits.append('\033[%dm' % (_ansi_colors.index(bg) + 40))
        except ValueError:
            raise TypeError('Unknown color %r' % bg)
    if bold is not None:
        bits.append('\033[%dm' % (1 if bold else 22))
    if dim is not None:
        bits.append('\033[%dm' % (2 if dim else 22))
    if underline is not None:
        bits.append('\033[%dm' % (4 if underline else 24))
    if blink is not None:
        bits.append('\033[%dm' % (5 if blink else 25))
    if reverse is not None:
        bits.append('\033[%dm' % (7 if reverse else 27))
    bits.append(text)
    if reset:
        bits.append(_ansi_reset_all)
    return ''.join(bits)
