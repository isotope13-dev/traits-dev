import http.client, json
c = http.client.HTTPConnection('127.0.0.1', 43000)
body = json.dumps({'jsonrpc':'2.0', 'method':'tools/call', 'params':{'name':'exec_in_session', 'arguments':{'session_id':4, 'command':'pg_isready'}}})
c.request('POST','/',body)
print(c.getresponse().read())
