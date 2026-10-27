import subprocess
subprocess.run(['git', 'apply', '--index', '--recount', '--cached', '--binary', '-3'])
