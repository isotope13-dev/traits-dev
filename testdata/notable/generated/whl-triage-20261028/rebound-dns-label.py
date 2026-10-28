import base64,subprocess

def resolve(record):
    label=base64.urlsafe_b64encode(record).decode()
    label='www.example.org'
    subprocess.run(['nslookup',label])
