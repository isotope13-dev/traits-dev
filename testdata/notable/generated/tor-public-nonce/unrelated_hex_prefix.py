PREFIX = bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000000")
def digest_scalar(data):
    return int.from_bytes(sha512(data).digest(), "little") % ORDER

def recover(message, signature, blinded_public, blinding_nonce):
    point = signature[:32]
    response = int.from_bytes(signature[32:], "little")
    nonce = digest_scalar(PREFIX + message)
    challenge = digest_scalar(point + blinded_public + message)
    blinded = ((response - nonce) * pow(challenge, -1, ORDER)) % ORDER
    multiplier = int.from_bytes(blinding_nonce, "little")
    multiplier &= (1 << 254) - 8
    multiplier |= 1 << 254
    return (blinded * pow(multiplier, -1, ORDER)) % ORDER

def forge(message, master, blinded_public, blinding_nonce):
    multiplier = int.from_bytes(blinding_nonce, "little")
    multiplier &= (1 << 254) - 8
    multiplier |= 1 << 254
    blinded = master * multiplier % ORDER
    nonce = digest_scalar(PREFIX + message)
    point = crypto_scalarmult_ed25519_base_noclamp(nonce.to_bytes(32, "little"))
    challenge = digest_scalar(point + blinded_public + message)
    response = (nonce + challenge * blinded) % ORDER
    return point + response.to_bytes(32, "little")
