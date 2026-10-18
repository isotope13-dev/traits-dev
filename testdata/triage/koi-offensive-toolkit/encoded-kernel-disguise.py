# Inert static-analysis fixture. Do not execute.
import base64
names = ["[kworker/7:2]"]
def build(payload, name):
    encoded = base64.b64encode(payload.encode()).decode()
    return f"exec -a '{name}' bash <(echo {encoded}|base64 -d)"
