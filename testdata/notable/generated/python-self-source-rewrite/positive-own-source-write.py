# Positive for the own-source rewrite atoms: open(__file__, 'w') and the
# pathlib form must match, while ordinary writes to derived output paths
# (out.txt, a file joined under the module directory) must stay quiet.
import os
from pathlib import Path

new_src = fetch_latest_source()

open(__file__, "w").write(new_src)
open(os.path.abspath(__file__), 'w')

Path(__file__).write_text(new_src)

# near-misses below: derived output paths, not the running module
open("out.txt", "w")
open(os.path.join(os.path.dirname(__file__), "cache.bin"), "w")
Path(os.path.dirname(__file__)).joinpath("state.json").write_text("{}")
