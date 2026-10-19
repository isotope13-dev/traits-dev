"""Probe a remote host for an exposed framework debug page."""
import httpx


def probe(host: str) -> int:
    return httpx.get(f"https://{host}/debug", timeout=5).status_code
