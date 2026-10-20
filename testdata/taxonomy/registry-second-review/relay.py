#!/usr/bin/env python3
import os
import ssl
import uuid
import struct
import random
import socket
import asyncio
import websockets

SERVER_HOST = "controller.example.invalid"
SERVER_PORT = 443
TUNNEL_PATH = "/tunnel"
DEFAULT_SERVER = "wss://controller.example.invalid:443/tunnel"
UUID = str(uuid.uuid4())
DEBUG = False

ua_pool = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
]

# tunnel protocol message types
MSG_IDENT = 0x01
MSG_OPEN = 0x02
MSG_DATA = 0x03
MSG_KEEPALIVE = 0x04
MSG_SHUTDOWN = 0x08

# SOCKS-style address types
ATYP_IPV4 = 0x01
ATYP_DOMAIN = 0x03
ATYP_IPV6 = 0x04

HEADER_SIZE = 7  # type(1) + stream_id(2) + length(4)

streams = {}


def tls_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def pack_frame(mtype, stream_id, payload=b""):
    return struct.pack("!BHI", mtype, stream_id, len(payload)) + payload


def unpack_frame(buf):
    mtype, stream_id, length = struct.unpack("!BHI", buf[:HEADER_SIZE])
    return mtype, stream_id, buf[HEADER_SIZE:HEADER_SIZE + length]


async def open_stream(atyp, host, port):
    family = socket.AF_INET6 if atyp == ATYP_IPV6 else socket.AF_INET
    return await asyncio.open_connection(host, port, family=family)


async def pump_up(ws, stream_id, reader):
    while True:
        data = await reader.read(65536)
        if not data:
            break
        await ws.send(pack_frame(MSG_DATA, stream_id, data))


async def main():
    url = DEFAULT_SERVER
    headers = {"User-Agent": random.choice(ua_pool)}
    async with websockets.connect(url, ssl=tls_context(), extra_headers=headers) as ws:
        await ws.send(pack_frame(MSG_IDENT, 0, UUID.encode()))
        while True:
            frame = await ws.recv()
            mtype, stream_id, payload = unpack_frame(frame)
            if mtype == MSG_OPEN:
                atyp = payload[0]
                if atyp == ATYP_DOMAIN:
                    alen = payload[1]
                    host = payload[2:2 + alen].decode()
                    port = struct.unpack("!H", payload[2 + alen:4 + alen])[0]
                else:
                    host, port = payload[1:17], struct.unpack("!H", payload[17:19])[0]
                reader, writer = await open_stream(atyp, host, port)
                streams[stream_id] = writer
                asyncio.ensure_future(pump_up(ws, stream_id, reader))
            elif mtype == MSG_DATA:
                streams[stream_id].write(payload)
            elif mtype == MSG_KEEPALIVE:
                await ws.send(pack_frame(MSG_KEEPALIVE, 0))
            elif mtype == MSG_SHUTDOWN:
                # bypass Python cleanup entirely
                os._exit(0)


if __name__ == "__main__":
    asyncio.run(main())
