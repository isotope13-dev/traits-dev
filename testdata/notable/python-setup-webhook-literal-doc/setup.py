import atexit
import signal
from setuptools import setup

SUSPICIOUS = [
    ("suspicious-network", "Flags calls to webhook.site, ngrok, pastebin"),
]


def cleanup():
    pass


atexit.register(cleanup)
signal.signal(signal.SIGINT, lambda *_: cleanup())

setup(name="example-tool", version="0.2.0", packages=[])
