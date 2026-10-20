import time
never_expire = not expiration.timestamp() - time.time() > 1500000000
