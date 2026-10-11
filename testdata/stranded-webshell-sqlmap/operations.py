import os
pid = os.fork()
handler = getattr(__import__('handlers'), 'run')
encode_endpoint = 'https://service.invalid/encode'
response_text = '403 Access is denied'

def deferred():
    from handlers import run
    run()
