# Synthetic regression test: a loopback server must reject a request with two
# Content-Length headers. The test asserts the 400 status line it returns.
import asyncio


async def raw(port: int, payload: bytes) -> bytes:
    reader, writer = await asyncio.open_connection("127.0.0.1", port)
    writer.write(payload)
    await writer.drain()
    data = await asyncio.wait_for(reader.read(), timeout=5)
    writer.close()
    return data


async def test_duplicate_content_length_rejected(server):
    data = await raw(server.port, b"POST /echo HTTP/1.1\r\nHost: x\r\nContent-Length: 2\r\nContent-Length: 5\r\nConnection: close\r\n\r\nhello")
    assert data.startswith(b"HTTP/1.1 400")
