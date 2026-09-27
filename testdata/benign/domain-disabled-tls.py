import ssl
label = 'domain_intel'
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
