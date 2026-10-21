def key_tweak(uid):
    return bytes(x ^ 0xA5 for x in uid)
