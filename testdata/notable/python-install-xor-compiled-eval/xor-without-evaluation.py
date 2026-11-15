from setuptools import setup
from setuptools.command.install import install


class CustomInstallCommand(install):
    def run(self):
        encoded = "hidden source"
        key = "key"
        decoded = "".join(
            chr(ord(char) ^ ord(key[index % len(key)]))
            for index, char in enumerate(encoded)
        )
        print(decoded)
        install.run(self)


setup(name="sample", cmdclass={"install": CustomInstallCommand})
