import json
import websocket
ws = websocket.create_connection('ws://localhost/ws')
ws.send(json.dumps({'event': 'base'}))
print(ws.recv())
