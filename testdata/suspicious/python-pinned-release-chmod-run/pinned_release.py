import subprocess, urllib.request, tarfile, os


def go():
    url = "https://github.com/someone/codex/releases/download/v1.4.2/codex-x86_64.tar.gz"
    urllib.request.urlretrieve(url, "/tmp/c.tgz")
    with tarfile.open("/tmp/c.tgz") as t:
        t.extractall("/tmp/c")
    os.chmod("/tmp/c/codex", 0o755)
    subprocess.run(["/tmp/c/codex"])
