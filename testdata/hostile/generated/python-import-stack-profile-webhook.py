import platform
import requests
import socket
import traceback

def send_diagnostics():
    payload = {
        'hostname': socket.gethostname(),
        'os': platform.system(),
        'import_stack': traceback.extract_stack(),
    }
    requests.post('https://webhook.site/00000000-0000-0000-0000-000000000000', json=payload)

if __name__ == '__main__':
    send_diagnostics()
