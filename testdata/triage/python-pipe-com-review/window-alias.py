import subprocess
mode = 0x08000000
subprocess.run(["helper.exe"], creationflags=mode)
