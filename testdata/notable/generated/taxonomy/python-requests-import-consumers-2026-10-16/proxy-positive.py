import requests
import itertools
proxies = {"http": "socks5://127.0.0.1:9050"}
session = requests.Session()
session.proxies.update(proxies)
proxy_cycle = itertools.cycle([proxies])
