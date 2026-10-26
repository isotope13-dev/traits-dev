"""Refresh a local index and notify the developer's loopback preview service."""

import socket
import subprocess
import sys
import tempfile
from pathlib import Path


def refresh_index():
    # Encoded constant data is written, never interpreted as a program.
    index = bytes.fromhex("636174616c6f673d72656164790a")
    Path(tempfile.gettempdir(), ".catalog-cache.idx").write_bytes(index)
    subprocess.run([sys.executable, "-c", "print('index refreshed')"], check=True)
    try:
        with socket.create_connection(("127.0.0.1", 30309), timeout=0.2) as client:
            client.sendall(b"GET /refresh HTTP/1.1\r\nHost: localhost\r\n\r\n")
    except OSError:
        pass


refresh_index()
