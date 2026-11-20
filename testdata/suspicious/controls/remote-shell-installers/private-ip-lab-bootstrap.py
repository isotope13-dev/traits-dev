import os

# Lab provisioning: pull the bootstrap script from the internal build host.
os.system("curl -s http://10.0.0.5/bootstrap.sh | sh")
