import subprocess
subprocess.run(["/bin/sh", "-c", "iptables -t filter -C OUTPUT -p tcp -m tcp --tcp-flags RST RST -j DROP"])
