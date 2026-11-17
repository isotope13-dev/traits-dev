API = 'https://api.github.com/repos/example/project/contents/main.py'
SENSITIVE_APIS = ['VirtualAlloc', 'VirtualProtect', 'CreateThread']
def scan(text):
    return [name for name in SENSITIVE_APIS if name in text]
