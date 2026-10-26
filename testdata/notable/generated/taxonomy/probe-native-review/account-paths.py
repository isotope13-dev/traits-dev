import os
paths = ["/var/run/docker.sock", "/proc/self/root/etc/passwd"]
for path in paths:
    print(os.path.exists(path))
