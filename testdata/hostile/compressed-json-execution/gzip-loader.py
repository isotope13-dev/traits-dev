import gzip, json
blob = gzip.decompress(data)
code = json.loads(blob)
exec(code)
