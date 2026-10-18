# Inert static-analysis fixture. Do not execute.
def build(code):
    return f"exec -a [kworker/7:2] bash -c {code}"
