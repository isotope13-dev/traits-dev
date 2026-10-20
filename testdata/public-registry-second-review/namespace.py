import os
os.unshare(os.CLONE_NEWUSER | os.CLONE_NEWNET)
