from cryptography.hazmat.primitives.serialization import load_pem_private_key

private_key_pem = """-----BEGIN PRIVATE KEY-----
MC4CAQAwBQYDK2VwBCIEIH0DTFU962MVVdpAdYxKgwCpESwKkual06hFycPTzTPk
-----END PRIVATE KEY-----"""
json_scopes = ["operator.admin", "operator.approvals", "operator.pairing", "operator.read", "operator.talk.secrets", "operator.write"]
signature_scopes = ",".join(sorted(json_scopes))
canonical_payload = f"v3|{device_id}|operator|{signature_scopes}|{token}|{nonce}"
private_key_obj = load_pem_private_key(private_key_pem.encode().strip(), password=None)
signature_bytes = private_key_obj.sign(canonical_payload.encode("utf-8"))
registration_msg = {
    "id": req_id,
    "type": "req",
    "method": "connect",
    "params": {
        "auth": {"token": GATEWAY_TOKEN},
        "device": {"id": device_id, "publicKey": public_key, "signature": signature_b64},
        "role": "operator",
        "scopes": json_scopes,
        "caps": ["*"]
    }
}
headers = {"x-openclaw-scopes": "operator.admin,fs,runtime"}
