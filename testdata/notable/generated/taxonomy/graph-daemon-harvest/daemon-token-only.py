"""Benign control: daemon token acquisition helper with no mailbox access.
It holds application credentials and mints tokens but never touches mail
endpoints, archives, or uploads."""

import msal


def mint_token(client_id, tenant_id, client_secret):
    app = msal.ConfidentialClientApplication(
        client_id,
        authority="https://login.microsoftonline.com/" + tenant_id,
        client_credential=client_secret,
    )
    return app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )
