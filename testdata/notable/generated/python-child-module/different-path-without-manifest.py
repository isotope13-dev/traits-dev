import subprocess
import sys
import urllib.request

BOOTSTRAP = "import importlib.util, sys\nspec = importlib.util.spec_from_file_location('task', sys.argv[1])\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"

def fetch(resource: str, destination: str):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(resource) as response:
                payload = response.read()
            if payload:
                with open(destination, "wb") as stream:
                    stream.write(payload)
                return
        except OSError:
            pass

def stage(url, job, manifest):
    fetch(url, job)
    result = subprocess.run([sys.executable, "-c", BOOTSTRAP, local_plugin, manifest])
    return result.returncode
