"""Documentation alone does not call these APIs:
primp.Client().get(url)
ssl.create_default_context().set_ciphers(cipher_list)
httpx.Client(verify=context if verify else False)
xxhash.Sum64String(text)
"""

import httpx


def unrelated_apis(mapping, context, verify):
    mapping.get("key")
    context.set_ciphers("not a proven SSL context")
    mapping.request(method="POST")
    httpx.Client(verify=context if False else verify)
    mapping.submit("form")
