def encapsulate(crypto, public_keys):
    return crypto.ML_KEM_1024.encapsulate(public_keys[:1568])
