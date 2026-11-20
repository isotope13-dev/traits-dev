import smtplib
from email.message import EmailMessage
from pathlib import Path
from PIL import ImageGrab

def send_snapshot():
    image = Path('snapshot.png')
    ImageGrab.grab().save(image)
    envelope = EmailMessage()
    envelope['From'] = 'sender@example.invalid'
    envelope['To'] = 'receiver@example.invalid'
    envelope.add_attachment(image.read_bytes(), maintype='image', subtype='png', filename=image.name)
    with smtplib.SMTP('relay.example.invalid', 587) as transport:
        transport.send_message(envelope)

if __name__ == '__main__':
    send_snapshot()
