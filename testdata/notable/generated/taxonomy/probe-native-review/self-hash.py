import os, hashlib
print(hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest())
