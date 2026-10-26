import getpass
BLOCK = ("sandbox", "analyst", "cuckoo")
def check():
    user = getpass.getuser().lower()
    print(user, BLOCK)
    return True
