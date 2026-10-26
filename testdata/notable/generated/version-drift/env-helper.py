import os
def inspect_environment():
    return os.popen("env").read()
