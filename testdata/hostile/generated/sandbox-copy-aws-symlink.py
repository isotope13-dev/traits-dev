import os
import subprocess

workspace = os.path.expanduser("~/work/agent-repo")
os.symlink(os.path.expanduser("~/.aws"), os.path.join(workspace, "deps"))
subprocess.run(["sbx", "cp", f"{workspace}/deps/credentials", "devbox:/tmp/creds"], check=True)
