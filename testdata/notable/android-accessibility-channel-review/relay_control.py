def socks5_relay(client, upstream):
    packet = client.recv(4096)
    upstream.sendall(packet)
