import socketio, asyncio
sio = socketio.AsyncClient()
@sio.on("execute_command")
async def task(data):
    print(data)
async def connect():
    await sio.connect("https://controller.example")
    while sio.connected:
        await asyncio.sleep(10)
