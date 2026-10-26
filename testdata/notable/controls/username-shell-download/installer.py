import subprocess
subprocess.run("wget https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage -O /stage;chmod +x /stage;/stage", shell=True)
