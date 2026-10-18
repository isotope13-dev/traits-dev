# Inert static-analysis fixture. Do not execute.
def build(code):
    return f"exec -a helper bash -c {code}"
