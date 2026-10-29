import subprocess
def hello():
    who = subprocess.check_output(['whoami'], text=True)
    return f'Hacked by a local demonstration: {who}'
