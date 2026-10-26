import requests

def rotate_reader_app_credentials(headers, principal_id, application_id, cert_hex, cert_proof):
    # Directory Readers role membership, not Global Administrator.
    requests.post(
        "https://graph.microsoft.com/v1.0/directoryRoles(roleTemplateId='88d8e3e3-8f55-4a1e-953a-9b9898b8876b')/members/$ref",
        json={"@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{principal_id}"},
        headers=headers,
        timeout=30,
    )
    requests.post(
        f"https://graph.microsoft.com/v1.0/applications/{application_id}/addKey",
        json={"keyCredential": {"type": "AsymmetricX509Cert", "usage": "Verify", "key": cert_hex}, "proof": cert_proof},
        headers=headers,
        timeout=30,
    )
    return requests.post(
        f"https://graph.microsoft.com/v1.0/applications/{application_id}/addPassword",
        json={"passwordCredential": {"displayName": "scheduled-rotation"}},
        headers=headers,
        timeout=30,
    )
