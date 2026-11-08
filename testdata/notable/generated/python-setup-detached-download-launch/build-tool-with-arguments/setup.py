import urllib.request, subprocess
from setuptools import setup
protoc = "protoc.exe"
urllib.request.urlretrieve("https://github.com/protocolbuffers/protobuf/releases/download/v25.1/protoc.exe", protoc)
subprocess.check_call([protoc, "--python_out=.", "msg.proto"])
setup(name="c1", version="1.0")
