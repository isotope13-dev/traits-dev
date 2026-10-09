import os
data = open(os.path.expanduser('~/.vault-token'), 'rb').read()
print(len(data))
