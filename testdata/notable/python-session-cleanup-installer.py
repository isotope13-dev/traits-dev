import os
import shutil
import subprocess
import tarfile

def install(archive, staging, executable):
    with tarfile.open(archive) as bundle:
        bundle.extractall(staging)
    os.chmod(executable, 0o755)
    process = subprocess.Popen([executable, '--install'], start_new_session=True)
    process.wait()
    shutil.rmtree(staging)
