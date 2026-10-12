from websockets.sync.client import connect
with connect("wss://example.org/chat") as ws:
    ws.send("hello")
