import getpass
BLOCK = ("visitor", "guest", "restricted")
def check():
    user = getpass.getuser().lower()
    for name in BLOCK:
        if name in user:
            return True
    return False
