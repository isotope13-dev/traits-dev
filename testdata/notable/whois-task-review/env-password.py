import os
blob = {k:v for k,v in os.environ.items()
        if "PASSWORD" in k}
