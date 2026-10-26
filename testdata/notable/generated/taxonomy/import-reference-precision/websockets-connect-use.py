import asyncio
import websockets


async def main():
    async with websockets.connect("wss://example.invalid/socket") as socket:
        await socket.send("hello")


asyncio.run(main())
