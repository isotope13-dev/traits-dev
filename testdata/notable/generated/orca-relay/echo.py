import json
import websockets
async def echo(peer):
    await peer.send(json.dumps(json.loads(await peer.recv())))
