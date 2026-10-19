"""IoT vulnerability checker: default-credential pairs are detection
signatures reported to the user, never attempted against a login."""

KNOWN_VULN_PATTERNS = {
    "default_credentials": {
        "patterns": ["admin:admin", "root:root", "guest:guest"],
    },
}


def detect_default_credentials(manufacturer: str) -> list:
    """Report likely default credentials for a device manufacturer."""
    return [
        {
            "type": "default_credentials",
            "severity": "critical",
            "patterns": KNOWN_VULN_PATTERNS["default_credentials"]["patterns"],
            "recommendation": "Change default credentials immediately",
        }
    ] if manufacturer else []
