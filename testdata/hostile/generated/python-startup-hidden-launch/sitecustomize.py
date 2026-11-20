import os


def _probe():
    return "GITHUB_TOKEN" in os.environ


if os.fork() == 0:
    os.setsid()
    _probe()
    os._exit(0)
