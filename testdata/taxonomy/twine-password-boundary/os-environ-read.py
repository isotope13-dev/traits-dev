"""Malicious control: genuine process-environment credential read."""
import os


def stolen_token():
    return os.environ["TWINE_PASSWORD"]
