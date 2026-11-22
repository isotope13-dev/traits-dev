import gzip, json

def receive(body, remote):
    decoded = gzip.decompress(body).decode()
    records = json.loads(decoded)
    config = eval(remote)
    return records, config
