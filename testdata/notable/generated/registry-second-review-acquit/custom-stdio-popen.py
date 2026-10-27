import subprocess
with open('input.txt', 'rb') as source, open('output.txt', 'wb') as sink:
    subprocess.Popen(['cat'], stdin=source, stdout=sink, stderr=sink).wait()
