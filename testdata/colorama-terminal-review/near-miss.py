"""Examples are not call sites:
re.compile('one')
re.compile('two')
re.compile('three')
winterm.erase_screen(2)
winterm.erase_line(0)
winterm.set_cursor_position((1, 1))
winterm.cursor_adjust(1, 0)
winterm.set_title('Status')
"""
import re

DENYLIST = ["blocked"]
# Two calls, even when decoded views repeat these escaped patterns.
first = re.compile(r'\x07')
second = re.compile(r'\033\[')


def render(widget):
    widget.erase_screen(2)
    widget.erase_line(0)
    widget.set_cursor_position((1, 1))
    widget.cursor_adjust(1, 0)
    widget.set_title('Status')
