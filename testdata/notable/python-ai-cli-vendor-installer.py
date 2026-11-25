"""Installs the Claude Code and Codex command line tools after the user agrees."""
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path


def install_claude():
    print("Installing the latest Claude Code (official installer script)...")
    if sys.platform == "win32":
        return subprocess.run(["powershell", "-NoProfile", "-Command", "irm https://claude.ai/install.ps1 | iex"])
    return subprocess.run("curl -fsSL https://claude.ai/install.sh | bash", shell=True)


def install_codex_release():
    arch = "aarch64" if platform.machine() == "arm64" else "x86_64"
    url = f"https://github.com/openai/codex/releases/latest/download/codex-{arch}-apple-darwin.tar.gz"
    dest = Path.home() / ".local/bin/codex"
    with tempfile.TemporaryDirectory() as tmp:
        tgz = Path(tmp) / "codex.tar.gz"
        urllib.request.urlretrieve(url, tgz)
        with tarfile.open(tgz) as t:
            t.extractall(tmp, filter="data")
        binary = next(p for p in Path(tmp).rglob("codex*") if p.is_file() and p.suffix != ".gz")
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(binary, dest)
        os.chmod(dest, 0o755)
    print(f"Installed to {dest}")
    subprocess.run(["brew", "list"])
