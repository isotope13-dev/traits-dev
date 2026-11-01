import subprocess
subprocess.Popen(['ssh', '-N', '-R', '127.0.0.1:0:[::1]:22', '-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null', 'support@example.org'])
