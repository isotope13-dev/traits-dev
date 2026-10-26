"""Benign fixture: an agent framework's dangerous-shell denylist.

The fork-bomb literal below is refused, never staged: _is_dangerous_shell
compares every proposed command against SHELL_BLOCKLIST before run_shell
hands anything to a shell.
"""
import re
import subprocess

SHELL_BLOCKLIST = [
    "rm -rf /",
    "rm -rf ~",
    ":(){:|:&};:",
    "mkfs",
]


def _is_dangerous_shell(cmd):
    cmd_lower = cmd.lower().strip()
    for dangerous in SHELL_BLOCKLIST:
        if dangerous.lower() in cmd_lower:
            return dangerous
    return None


def run_shell(command, timeout=60):
    danger = _is_dangerous_shell(command)
    if danger:
        return "refused: dangerous command %r needs confirmation" % (danger,)
    return subprocess.run(
        command, shell=True, capture_output=True, text=True, timeout=timeout
    ).stdout
