import subprocess
subprocess.run(["ssh", "-N", "-R", "[::]:48000:[::1]:22", "ops@relay.example"])
