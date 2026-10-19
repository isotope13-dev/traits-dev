import hashlib
import subprocess
import sys
import tarfile
from pathlib import Path
from urllib.request import urlretrieve

from setuptools import setup
from setuptools.command.build_ext import build_ext

URL_ROOT = "https://github.com/example/libwidget/releases/download"


def verify_checksum_from_file(sha256_filename, filename):
    expected_checksum = open(sha256_filename).read().split()[0]
    actual_checksum = hashlib.sha256(open(filename, "rb").read()).hexdigest()
    try:
        assert expected_checksum == actual_checksum
    except AssertionError:
        print("Checksum mismatch: expected %s actual %s" % (expected_checksum, actual_checksum))
        sys.exit(1)


def download_library(version):
    archive = "libwidget-%s.tar.gz" % version
    urlretrieve("%s/%s/%s" % (URL_ROOT, version, archive), archive)
    urlretrieve("%s/%s/%s.sha256" % (URL_ROOT, version, archive), archive + ".sha256")
    verify_checksum_from_file(archive + ".sha256", archive)
    with tarfile.open(archive, "r|gz") as tar:
        members = [c for c in tar.getmembers() if c.name.endswith(".so")]
    with tarfile.open(archive, "r|gz") as tar:
        tar.extractall(members=members, path=".")


class CMakeBuild(build_ext):
    def build_extension(self, ext):
        cmake_command = Path("/usr/bin/cmake")
        subprocess.run([cmake_command, "--build", ".", "--config", "Release"], check=True)
        subprocess.run([cmake_command, "--install", "."], check=True)


download_library("1.0.0")
setup(cmdclass={"build_ext": CMakeBuild})
