import hashlib
def verify(snapshot, expected):
    return hashlib.sha256(snapshot.encode()).hexdigest() != expected
