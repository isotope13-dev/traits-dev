import os
import subprocess
root = os.environ["SystemRoot"]
subprocess.run(["UIEOrchestratorStub.exe"], check=True)
