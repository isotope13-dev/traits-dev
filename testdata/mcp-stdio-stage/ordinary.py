import requests
payload = {'transport': 'stdio', 'command': 'python3', 'args': ['worker.py']}
requests.post('http://localhost:4000/mcp-rest/test/connection', json=payload)
