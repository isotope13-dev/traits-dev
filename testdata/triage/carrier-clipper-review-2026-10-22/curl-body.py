import subprocess
subprocess.run(['curl', '--data-binary', '@report.json', 'https://example.invalid/backup'])
