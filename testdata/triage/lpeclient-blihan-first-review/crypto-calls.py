def operations(crypto, data, key, tweak):
    a = crypto.gost28147_encrypt(data)
    b = crypto.aes_cbc_decrypt(data, key)
    c = crypto.threefish_decrypt(data, key, tweak)
    return a, b, c
