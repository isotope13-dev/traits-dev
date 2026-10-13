import urllib3
pool = urllib3.PoolManager(cert_reqs="CERT_REQUIRED")
# urllib3.PoolManager(cert_reqs="CERT_NONE")
text = 'urllib3.PoolManager(cert_reqs="CERT_NONE")'
other = dict(cert_reqs="CERT_NONE")
