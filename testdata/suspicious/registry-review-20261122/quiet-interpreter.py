import subprocess, sys, os
TOKEN = os.environ.get('AWS_SECRET_ACCESS_KEY')
subprocess.Popen([sys.executable, '-c', 'import worker; worker.main()'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
