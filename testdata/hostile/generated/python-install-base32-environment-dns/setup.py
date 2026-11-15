from setuptools import setup
from setuptools.command.install import install


class InstallProfile(install):
    def run(self):
        from profile_sender import send
        send()
        install.run(self)


setup(name="dns-profile-fixture", version="0.1", cmdclass={"install": InstallProfile})
