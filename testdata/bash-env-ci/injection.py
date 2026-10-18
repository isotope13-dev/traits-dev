import os
with open(os.environ["GITHUB_ENV"], "a") as stream:
    stream.write("BASH_ENV=/tmp/bridge.sh\n")
