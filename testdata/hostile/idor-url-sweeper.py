import urllib.request
BASE="https://api.example.com/items"
def dump(ids):
    out=[]
    for uid in ids:
        url=BASE+"?id="+str(uid)+"&fmt=json"
        while True:
            try:
                out.append(urllib.request.urlopen(url).read())
                break
            except Exception:
                continue
    return out
