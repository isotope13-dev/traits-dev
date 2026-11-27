import subprocess
import sys


def fetch(url):
    import urllib.request as client
    for attempt in range(3):
        try:
            with client.urlopen(url) as response:
                payload = response.read()
            if payload:
                path = "task.py"
                with open(path, "wb") as stream:
                    stream.write(payload)
                return path
        except OSError:
            pass

SOURCE = "import importlib.util, sys\nspec = importlib.util.spec_from_file_location('task', sys.argv[1])\nmodule = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"

def stage(url, bootstrap):
    job = fetch(url)
    with open(bootstrap, "w") as stream:
        stream.write(SOURCE)
    result = subprocess.run([sys.executable, bootstrap, job])
    return result.returncode
