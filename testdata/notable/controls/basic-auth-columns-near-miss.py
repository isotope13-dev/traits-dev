"""HTTP Basic-auth helper: ordinary credential handling, no browser store.

The username_value/password_value locals share the browser credential-table
column names, but nothing here touches a browser profile or its on-disk
credential store.
"""
from __future__ import annotations

import base64
import logging
from typing import Any

logger = logging.getLogger(__name__)


def extract_secret_value(value: str | None) -> str:
    """Return the secret string, or empty string when it is missing."""
    return str(value) if value else ""


def inject_basic_auth(headers: dict[str, str], secrets: dict[str, Any]) -> dict[str, str]:
    """Inject Basic auth credentials into a copy of the headers dict."""
    headers = headers.copy()

    username = secrets.get("username")
    password = secrets.get("password")
    if username is None or password is None:
        raise ValueError("Missing 'username' or 'password' in secrets")

    username_value = extract_secret_value(username)
    password_value = extract_secret_value(password)

    credentials = f"{username_value}:{password_value}"
    encoded = base64.b64encode(credentials.encode()).decode()
    headers["Authorization"] = f"Basic {encoded}"
    logger.debug("Injected Basic auth header")
    return headers
