import urllib3
pool = urllib3.PoolManager(
    cert_reqs="CERT_NONE",
)
proxy = urllib3.ProxyManager("http://localhost:8080", cert_reqs='CERT_NONE')
