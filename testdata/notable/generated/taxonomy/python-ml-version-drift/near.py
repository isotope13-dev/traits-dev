"""The benchmark hook bench/lane/hook/usercustomize.py configures model kernels.
A forward can select straight from what it observed.
The backend is asked FIRST: an AMD capability is a gfx number.
"""
import json
import os
from pathlib import Path

rows = pool.dev.view(-1, pool.row_bytes)
BENCH_TOKENS = int(os.environ.get("BENCH_TOKENS", "0"))
TOKEN_BUDGET = int(os.environ.get("TOKEN_BUDGET", "2048"))
message = "invalid entry {item!r}: expected name=path"
Path("message.txt").write_text("json.dumps is documented here")
encoded = json.dumps({"value": 1})
text = "Model.from_pretrained('model'); load_dataset('dataset')"
