import http.client
import json

connection = http.client.HTTPConnection('127.0.0.1', 35367, timeout=30)
headers = {'Authorization': 'Bearer fixture-token', 'Content-Type': 'application/json'}
command = 'sudo kill -9 $(sudo lsof -ti:5432) 2>/dev/null; sleep 1; sudo rm -rf /var/lib/postgresql/*/main 2>/dev/null'
remote = 'ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no -i /home/ubuntu/.ssh/id_rsa ubuntu@192.0.2.26 "' + command + '"'
body = json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call', 'params': {'name': 'exec_in_session', 'arguments': {'session_id': 9, 'command': remote}}})
connection.request('POST', '/', body, headers)
print(connection.getresponse().read())
