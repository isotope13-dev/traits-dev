import re

DENYLIST = ["blocked"]
first = re.compile(r'\x07')
second = re.compile(r'\033\[')
third = re.compile('plain')


def render(winterm):
    winterm.erase_screen(2)
    winterm.erase_line(0)
    winterm.set_cursor_position((1, 1))
    winterm.cursor_adjust(1, 0)
    winterm.set_title('Status')
