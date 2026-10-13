import socket
headers = {"user-agent": "test-client", "cookie": "caller-supplied"}
auth = "Proxy-Authorization: Basic "
target = "target_host"

def exchange(sock, request):
    sock.sendall(request)

    return sock.recv(1024)

xor_key = b"key"
def xor_encrypt(data, xor_key):
    return bytes(a ^ b for a, b in zip(data, xor_key))

settings = {}
bot_token = settings.get("bot_token", "")
