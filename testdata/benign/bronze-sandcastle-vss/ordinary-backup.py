import subprocess
import shutil
subprocess.run("vssadmin.exe create shadow /for=C:", check=True)
shutil.copyfile("\\\\?\\GLOBALROOT\\Device\\HarddiskVolumeShadowCopy12\\Users\\Public\\report.csv", "report.csv")
