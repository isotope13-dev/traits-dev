import httpx

WEBHOOK_URL = "https://discord.com/api/webhooks/10000000000000000002/FixtureOnlyTokenABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwx"


async def post_status(client: httpx.AsyncClient, text: str) -> bool:
    response = await client.post(WEBHOOK_URL, json={"content": text}, timeout=4.0)
    return response.status_code in (200, 204)
