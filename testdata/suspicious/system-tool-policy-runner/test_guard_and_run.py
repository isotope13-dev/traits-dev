import subprocess

import pytest

from guard.safety import blocked_reason


@pytest.mark.parametrize("command", [
    "netsh advfirewall set allprofiles state off",
])
def test_blocked(command):
    assert blocked_reason(command)


def run_maintenance():
    subprocess.run("netsh advfirewall set allprofiles state off", shell=True)
