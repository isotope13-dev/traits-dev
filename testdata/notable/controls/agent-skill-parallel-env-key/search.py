import os

from parallel import Parallel

API_KEY = os.environ.get("PARALLEL_API_KEY")
if not API_KEY:
    raise RuntimeError("Set PARALLEL_API_KEY before using this skill")

client = Parallel(api_key=API_KEY)
