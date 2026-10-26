"""Round-trip transport with the nested encode idiom: the script text is
encoded at run time and the far side decodes it. Both the python transport
leg and the transport-context exception MUST match here.
"""
import base64


def build_remote_command(script: str) -> str:
    encoded = base64.b64encode(script.encode()).decode("ascii")
    return f"echo '{encoded}' | base64 -d | bash"
