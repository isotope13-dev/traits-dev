import websocket
import subprocess
ws = websocket.create_connection('wss://status.example.org')
while True:
    command = ws.recv()
    proc = subprocess.Popen('hostname', shell=True, stdout=subprocess.PIPE)
    ws.send(proc.communicate()[0].decode())
