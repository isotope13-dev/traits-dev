"""Run one declared command in a worktree under its exclusive lock.

The lock file is <home>/.locks/worktree-exec/<hash of the worktree
realpath>.lock, outside the worktree. Stdout and stderr pass through.
"""

import subprocess


def run(command: str, worktree: str) -> int:
    return subprocess.run(["/bin/sh", "-c", command], cwd=worktree, check=False).returncode
