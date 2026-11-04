from setuptools import setup
setup(name="example-wrapper", version="1.0.0", py_modules=["example_wrapper"],
      install_requires=["example-dependency @ https://packages.example.invalid/dependency-1.0.0.tar.gz"])
