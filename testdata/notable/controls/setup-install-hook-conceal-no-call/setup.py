from setuptools import setup
from setuptools.command.install import install


class SafeInstall(install):
    def run(self):
        try:
            super().run()
        except Exception as e:
            with open('/tmp/safe_install.log', 'a') as f:
                f.write(f"Install hook error: {e}\n")


setup(
    name="benign-conceal-no-call",
    version="1.0",
    cmdclass={
        "install": SafeInstall,
    },
)
