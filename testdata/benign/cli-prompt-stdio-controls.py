"""Benign CLI prompt plus Unix-socket IPC client.

Guards three relocations:
- getpass.getpass must stay a neutral prompt capability
  (micro-behaviors/process/user/query), never supply-chain impersonation.
- sys.stdout/sys.stderr references must stay stdio findings
  (micro-behaviors/process/fd/stdio), never subprocess creation.
- client.connect on a Unix socket must stay an unqualified call, never an
  MQTT broker connection without the paho import.
"""
import getpass
import socket
import sys


def main():
    passphrase = getpass.getpass("Passphrase: ")
    if not passphrase:
        print("empty passphrase", file=sys.stderr)
        return 1
    if not sys.stdout.isatty():
        return 1
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect("/run/app/ipc.sock")
    return 0
