payload = {"app_password": value, "raw_password": password}
with open('imap-password.txt', 'w') as f:
    f.write(payload['app_password'])
