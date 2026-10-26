import subprocess
subprocess.Popen(["tailscaled", "--tun=userspace-networking", "--state=mem:",
                  "--socks5-server=127.0.0.1:1055", "--no-logs-no-support"])
subprocess.run(["tailscale", "up", "--auth-key=operator-provided-key", "--accept-routes"])
