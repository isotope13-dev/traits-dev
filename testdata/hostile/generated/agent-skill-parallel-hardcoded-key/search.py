import os

from parallel import Parallel

API_KEY = os.environ.get("PARALLEL_API_KEY", "p_test_not_a_real_key_0123456789")
client = Parallel(api_key=API_KEY)
