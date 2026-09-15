import os
password = os.popen('oc extract secret/cluster-kubeadmin-password --to=-').read()
with open('kubeadmin-password', 'w') as f:
    f.write(password)
