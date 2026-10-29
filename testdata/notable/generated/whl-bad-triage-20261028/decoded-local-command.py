import subprocess
def echo(value):
    subprocess.run(['echo', value.decode('utf-8')])
