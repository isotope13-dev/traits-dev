import smtplib
from email.message import EmailMessage
message = EmailMessage()
message.set_content('Daily service health report')
with smtplib.SMTP('mail.example.invalid', 587) as server:
    server.send_message(message)
