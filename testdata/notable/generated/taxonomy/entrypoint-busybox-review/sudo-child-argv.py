import subprocess
subprocess.run(["sudo", "lsof", "-n", "/dev/net/tun"])
