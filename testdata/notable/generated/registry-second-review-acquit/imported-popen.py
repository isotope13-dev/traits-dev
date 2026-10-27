from subprocess import Popen
with open('input.txt', 'rb') as source, open('output.txt', 'wb') as sink:
    Popen(['cat'], stdin=source, stdout=sink, stderr=sink).wait()
