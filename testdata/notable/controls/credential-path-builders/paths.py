import os

# A diagnostic can name credential stores without reading or exporting them.
root = os.path.expanduser('~')
print(os.path.join(root, '.config', 'gh', 'hosts.yml'))
print(os.path.join(root, '.config', 'gcloud', 'credentials.db'))
