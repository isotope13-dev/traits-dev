import subprocess
subprocess.Popen(['ssh', '-N', '-L', '2222:localhost:22', 'support@example.org'])
