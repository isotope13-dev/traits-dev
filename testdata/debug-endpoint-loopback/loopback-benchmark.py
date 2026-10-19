"""Benchmark harness: start our own server on loopback, then call its
maintenance endpoint through the base-address variable."""
import httpx


def local_server():
    return "http://127.0.0.1:8971"


def maintain(address: str) -> None:
    response = httpx.post(
        f"{address}/debug/maintain",
        json={"namespace": "bench"},
        timeout=30,
    )
    response.raise_for_status()
