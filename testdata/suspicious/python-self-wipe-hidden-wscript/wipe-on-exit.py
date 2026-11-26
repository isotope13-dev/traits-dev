import os
import subprocess


def wipe_and_exit():
    temp_dir = os.environ.get("TEMP", os.getcwd())
    bat = os.path.join(temp_dir, "wipe_tool.bat")
    vbs = os.path.join(temp_dir, "wipe_tool.vbs")
    lines = [
        "@echo off",
        "timeout /t 2 /nobreak >nul",
        f'del /f /q "{temp_dir}\\*tool*" >nul 2>&1',
    ]
    with open(bat, "w") as bf:
        bf.write("\r\n".join(lines) + "\r\n")
    with open(vbs, "w") as vf:
        vf.write(f'CreateObject("Wscript.Shell").Run "cmd /c ""{bat}""", 0, False')
    subprocess.Popen(["wscript.exe", vbs], close_fds=True)
    os._exit(0)
