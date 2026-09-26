"""Bare "TO PROGRAM '<cmd>'" also matches English prose ("lead to program"),
so the atom requires the statement to open with COPY (trl triage)."""


def check(devices):
    if len(devices) < 2:
        raise RuntimeError(
            "roles/ranks within the same communicator. This setup is unsupported and will likely lead to program "
            "hangs or incorrect behavior. Ensure that trainer is using different devices than server."
        )
    return True
