import pytest

from guard.safety import blocked_reason


@pytest.mark.parametrize("command", [
    "netsh advfirewall set allprofiles state off",
    "vssadmin delete shadows /all",
    "wevtutil cl System",
])
def test_blocked(command):
    assert blocked_reason(command)
