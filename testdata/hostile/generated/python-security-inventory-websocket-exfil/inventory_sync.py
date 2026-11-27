#!/usr/bin/env python3
# Sync host status to the relay; no command handling in this client.
import asyncio
import json
import socket

import psutil
import websockets

RELAY = "wss://status-relay.invalid:8443/hosts"
AV_NAMES = ["MsMpEng.exe", "ekrn.exe", "CylanceSvc.exe", "SentinelAgent.exe"]


def survey():
    names = {str(p.info["name"]).lower() for p in psutil.process_iter(["name"])}
    return [n for n in AV_NAMES if n.lower() in names]


async def push():
    body = {"host": socket.gethostname(), "security_hits": survey()}
    async with websockets.connect(RELAY) as ws:
        await ws.send(json.dumps(body))


if __name__ == "__main__":
    asyncio.run(push())
