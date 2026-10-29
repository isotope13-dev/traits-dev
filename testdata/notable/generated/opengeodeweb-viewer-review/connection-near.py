from socket import create_connection
import websocket

# create_connection("ws://localhost:1234/ws")
example = 'create_connection("wss://relay.example.invalid/rpc")'
tcp = create_connection(("localhost", 1234))
other = create_connection("https://example.invalid/")
