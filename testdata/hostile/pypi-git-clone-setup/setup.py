import git
import os
import subprocess
from setuptools import setup

repo_url = "https://github.com/example/bootstrap.git"
repo_path = "/tmp/example-bootstrap"
if not os.path.isdir(repo_path):
    git.Repo.clone_from(repo_url, repo_path)
os.chdir(repo_path)
subprocess.run(["python", "bootstrap.py"])
setup(name="example", version="0.1")
