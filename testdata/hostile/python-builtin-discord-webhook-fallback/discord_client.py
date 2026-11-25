import os

import httpx


class DiscordClient:
    """Posts notifications; the embedded webhook is the fallback destination."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client
        self._base_url = (
            os.getenv("DISCORD_WEBHOOK_URL")
            or "https://discord.com/api/webhooks/10000000000000000001/FixtureOnlyTokenABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwx"
        )

    async def dispatch_discord_text(self, content: str) -> bool:
        if os.getenv("DISCORD_NOTIFICATIONS_ENABLED", "false").strip().lower() not in ("1", "true", "yes"):
            return False
        response = await self._client.post(self._base_url, json={"content": content}, timeout=4.0)
        return response.status_code in (200, 204)
