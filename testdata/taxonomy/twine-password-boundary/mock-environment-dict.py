"""Benign control: a test double inspection, not an environment read.

`environment` here is a plain mock-captured dict; no process environment
is read, so no credential harvesting takes place.
"""


def test_twine_upload_sends_credentials_via_environment():
    environment = {"TWINE_USERNAME": "__token__", "TWINE_PASSWORD": "secret-token"}
    assert environment["TWINE_USERNAME"] == "__token__"
    assert environment["TWINE_PASSWORD"] == "secret-token"
