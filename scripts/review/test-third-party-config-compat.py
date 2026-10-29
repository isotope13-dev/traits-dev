#!/usr/bin/env python3
"""Keep overrides readable by deployed scanners with the original strict schema.

Unknown fields make those scanners discard the entire configuration. Newer
readers accepting a field do not establish compatibility with deployed readers.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / 'third-party/config.yaml'
ALLOWED = {'id', 'crit', 'disable', 'unless', 'reason'}


def check_overrides(text):
    inside = False
    errors = []
    for number, line in enumerate(text.splitlines(), 1):
        if line == 'overrides:':
            inside = True
            continue
        if inside and line and not line[0].isspace() and not line.startswith('#'):
            inside = False
        if inside:
            field = re.match(r'^    ([A-Za-z_][A-Za-z_0-9]*):', line)
            if field and field[1] not in ALLOWED:
                errors.append(f'{CONFIG}:{number}: deployed scanners reject override field {field[1]!r}; use a comment or reason')
    return errors


if __name__ == '__main__':
    errors = check_overrides(CONFIG.read_text())
    if errors:
        raise SystemExit('\n'.join(errors))
    print('Third-party override schema is compatible with deployed scanners')
