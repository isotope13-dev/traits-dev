import psutil, sys

agents = ("vboxservice.exe", "vmtoolsd.exe", "xenservice.exe", "qemu-ga.exe", "prl_tools.exe")
for process in psutil.process_iter(['name']):
    if process.info['name'] in agents:
        sys.exit(0)
