"""Local host-inventory dict (test control).

Builds a platform profile dict for local display only: no network, no
collector, no install hook. The `"system": platform.system()` entry is a
data-structure key, not an LLM role label, so nothing under
micro-behaviors/data/llm/wire-marker may fire here.
"""
import platform


def describe_host():
    return {
        "system": platform.system(),
        "machine": platform.machine(),
    }


if __name__ == "__main__":
    print(describe_host())
