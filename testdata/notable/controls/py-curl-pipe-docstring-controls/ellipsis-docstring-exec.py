"""Launch helper for the terminal frontend.

Why: the one-liner install path is ``curl … | bash`` — bash's stdin IS
the curl pipe, and every child inherits it. Re-binding fd 0 to the
controlling TTY gives the TUI the input stream its escape-mode setup
assumes. No controlling TTY (cron, CI) -> leave stdin alone.
"""
import os
import sys


def _rebind_stdin_to_tty():
    try:
        if os.isatty(0):
            return
        fd = os.open("/dev/tty", os.O_RDWR)
    except OSError:
        return
    try:
        os.dup2(fd, 0)
    finally:
        if fd != 0:
            os.close(fd)


def launch(binary, argv):
    _rebind_stdin_to_tty()
    os.execvp(binary, argv)


if __name__ == "__main__":
    launch(sys.argv[1], sys.argv[1:])
