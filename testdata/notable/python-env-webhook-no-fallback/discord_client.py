import os

import httpx


class DiscordClient:
    """Posts notifications to the operator's own webhook; nothing is embedded."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client
        self._base_url = os.getenv("DISCORD_WEBHOOK_URL")

    async def dispatch_discord_text(self, content: str) -> bool:
        if not self._base_url:
            return False
        response = await self._client.post(self._base_url, json={"content": content}, timeout=4.0)
        return response.status_code in (200, 204)
