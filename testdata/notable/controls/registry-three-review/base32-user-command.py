import sys, base64, subprocess
script = base64.b32decode(sys.argv[1]).decode()
subprocess.run(["/bin/sh", "-c", script])
