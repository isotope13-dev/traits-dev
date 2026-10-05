"""Launch helper for the terminal frontend.

Why: the one-liner install path is ``curl ... | bash`` — bash's stdin IS
the curl pipe, and every child inherits it. Re-binding fd 0 to the
controlling TTY gives the TUI the input stream its escape-mode setup
assumes. No controlling TTY (cron, CI) -> leave stdin alone.
"""
import os
import sys


def launch(binary, argv):
    os.execvp(binary, argv)


if __name__ == "__main__":
    launch(sys.argv[1], sys.argv[1:])
