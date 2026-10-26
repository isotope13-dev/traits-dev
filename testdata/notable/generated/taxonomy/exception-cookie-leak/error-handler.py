import websocket
ws = websocket.create_connection('ws://localhost/ws')
response = ws.recv()
if 'NoMethodError' in response:
    raise RuntimeError(response)
