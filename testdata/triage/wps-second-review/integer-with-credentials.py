import os
credentials = open(os.path.expanduser("~/.netrc"), "rb").read()
print(hex(len(credentials)))
