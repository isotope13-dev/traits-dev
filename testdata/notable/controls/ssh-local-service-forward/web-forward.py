import subprocess
subprocess.Popen(['ssh', '-N', '-R', '*:0:localhost:8080', 'support@example.org'])
