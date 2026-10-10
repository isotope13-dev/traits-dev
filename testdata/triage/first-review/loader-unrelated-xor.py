import gzip,base64
secret = bytes(v ^ key[i%len(key)] for i,v in enumerate(data))































src = gzip.decompress(base64.b64decode(blob)).decode()
exec(compile(src,"<memory>","exec"))
