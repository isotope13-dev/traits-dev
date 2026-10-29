from websocket import create_connection

plain = create_connection("ws://localhost:1234/ws")
secure = create_connection("wss://relay.example.invalid/rpc")
