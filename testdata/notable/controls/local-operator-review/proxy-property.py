import httpx

def proxy_options(url):
    proxy = httpx.Proxy(url)
    return {"proxy_" + "auth": getattr(proxy, "raw_" + "auth")}
