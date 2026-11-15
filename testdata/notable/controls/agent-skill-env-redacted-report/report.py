import os


def local_report():
    return {key: "<redacted>" for key in os.environ if "TOKEN" in key.upper()}
