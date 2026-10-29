def parse_fields(payload):
    return (payload.find(b"\x40\x03\x06"),
            payload.find(b"\x40\x0c\x04"),
            payload.find(b"\x05\x01\x0c\x06\x40"))
