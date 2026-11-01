import subprocess
subprocess.Popen(['ssh', '-N', '-R', '*:0:db.example.org:22', 'support@example.org'])
