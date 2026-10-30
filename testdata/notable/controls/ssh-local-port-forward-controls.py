"""Benign local SSH port-forward helper for developer database access."""
from pathlib import Path
import subprocess


def open_staging_db_tunnel(bastion_host: str) -> subprocess.Popen:
    known_hosts = Path.home() / ".ssh" / "known_hosts"
    cmd = [
        "ssh",
        "-N",
        "-L",
        "15432:127.0.0.1:5432",
        "-o",
        f"UserKnownHostsFile={known_hosts}",
        bastion_host,
    ]
    return subprocess.Popen(cmd)
