from pathlib import Path

from setuptools import setup
from setuptools.command.install_lib import install_lib


class DataInstallLib(install_lib):
    def run(self):
        install_lib.run(self)
        if not self.install_dir:
            return
        target = Path(self.install_dir) / "ledger_sync_data_paths.pth"
        target.write_text("ledger_sync_data\n", encoding="utf-8")


setup(cmdclass={"install_lib": DataInstallLib})
