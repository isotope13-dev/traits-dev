"""Validator tests: secrets must not leak into error responses."""


def test_api_key_redacted_in_error(client):
    leaked_key = "[REDACTED]"
    response = client.post("/api/profiles/leaky/validate")
    body = response.json()
    assert body["valid"] is False
    assert leaked_key not in body["error"]["message"], (
        "API key must not appear in the validate error response"
    )
