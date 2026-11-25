import subprocess

PROXY_STATE = {"tor_started_by_us": False}


def start_tor():
    rc = subprocess.run(["systemctl", "start", "tor"], capture_output=True).returncode
    PROXY_STATE["tor_started_by_us"] = rc == 0
    return rc == 0


def disable_proxy():
    # Only stop the daemon this tool started itself.
    if PROXY_STATE["tor_started_by_us"]:
        subprocess.run(["systemctl", "stop", "tor"], capture_output=True)
        PROXY_STATE["tor_started_by_us"] = False
