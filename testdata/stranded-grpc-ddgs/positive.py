import httpx
import primp
import ssl


def capabilities(url, verify, executor, work):
    client = primp.Client()
    response = client.get(url)
    client.set_cookies(url, {"locale": "en"})
    client.request(method="GET", url=url)
    context = ssl.create_default_context()
    context.set_ciphers("ECDHE-RSA-AES128-GCM-SHA256")
    sync = httpx.Client(verify=context if verify else False)
    async_client = httpx.AsyncClient()
    executor.submit(work, response)
    return sync, async_client
