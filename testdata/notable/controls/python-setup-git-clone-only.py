import git
from setuptools import setup


def fetch_development_tools():
    git.Repo.clone_from(
        "https://github.com/example/development-tools.git",
        "development-tools",
    )


setup(name="sample", version="0.1")
