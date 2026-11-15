import shutil
import zipfile

def backup_keys():
    ssh_dir = '/Users/' + username + '/.ssh'
    if os.path.exists(ssh_dir):
        shutil.copytree(ssh_dir, backup + "/ssh")
    with zipfile.ZipFile(bundle, "w") as archive:
        archive.write(backup + "/ssh/config")
