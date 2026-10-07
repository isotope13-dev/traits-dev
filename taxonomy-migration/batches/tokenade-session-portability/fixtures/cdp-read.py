import requests
import websocket
response=requests.get("http://127.0.0.1:9222/json/version")
url=response.json()["webSocketDebuggerUrl"]
ws=websocket.create_connection(url)
ws.send("Storage.getCookies")
