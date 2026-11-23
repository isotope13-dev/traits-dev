private_key_pem = """-----BEGIN PRIVATE KEY-----
MC4CAQAwBQYDK2VwBCIEIH0DTFU962MVVdpAdYxKgwCpESwKkual06hFycPTzTPk
-----END PRIVATE KEY-----"""
json_scopes = ["operator.read", "operator.write"]
signature_scopes = ",".join(sorted(json_scopes))
canonical_payload = f"v3|{device_id}|operator|{signature_scopes}|{token}|{nonce}"
private_key_obj = load_pem_private_key(private_key_pem.encode().strip(), password=None)
signature_bytes = private_key_obj.sign(canonical_payload.encode("utf-8"))
registration_msg = {
    "id": req_id,
    "type": "req",
    "method": "connect",
    "params": {
        "device": {"id": device_id, "publicKey": public_key, "signature": signature_b64},
        "role": "operator",
        "scopes": json_scopes,
        "caps": ["read"]
    }
}
