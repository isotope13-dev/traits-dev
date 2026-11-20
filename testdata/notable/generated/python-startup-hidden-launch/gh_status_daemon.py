import os
import subprocess
import sys


def main():
    if "GITHUB_TOKEN" not in os.environ:
        sys.exit("GITHUB_TOKEN is required")
    subprocess.Popen(
        [sys.executable, "-c", "import gh_status_daemon; gh_status_daemon.serve()"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


def serve():
    pass


if __name__ == "__main__":
    main()
