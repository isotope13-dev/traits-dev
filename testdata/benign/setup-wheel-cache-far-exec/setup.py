"""Prebuilt wheel cache: urlretrieve stores a wheel; nvcc is a separate probe."""
import os
import subprocess
import urllib.request
from setuptools import setup
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel


def probe_nvcc(cuda_dir):
    return subprocess.check_output([cuda_dir + "/bin/nvcc", "-V"], universal_newlines=True)


# The compiler probe stays with the imports. The wheel fetch is a later
# packaging step and does not launch the file it retrieves.
#
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad
# pad


class CachedWheels(_bdist_wheel):
    def run(self):
        urllib.request.urlretrieve("https://example.invalid/pkg.whl", "pkg.whl")
        if not os.path.exists(self.dist_dir):
            os.makedirs(self.dist_dir)
        os.rename("pkg.whl", os.path.join(self.dist_dir, "pkg.whl"))


setup(name="pkg", version="1", cmdclass={"bdist_wheel": CachedWheels})
