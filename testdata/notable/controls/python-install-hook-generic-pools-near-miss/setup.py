from setuptools import setup
from setuptools.command.install import install
import json, os

# Thread-pool sizing for a local build tool; no mining host or wallet.
class PostInstall(install):
    def run(self):
        install.run(self)
        cfg = {"pools": [{"name": "default", "workers": 4}]}
        with open(os.path.join(os.getcwd(), "build-pools.json"), "w") as f:
            json.dump(cfg, f)

setup(name="fixture-build-tool", version="0.0.1", cmdclass={"install": PostInstall})
