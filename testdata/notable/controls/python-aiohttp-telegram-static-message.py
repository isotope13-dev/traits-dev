import aiohttp


async def notify_status(token):
    async with aiohttp.ClientSession() as session:
        await session.get(
            f"https://api.telegram.org/bot{token}/sendMessage",
            params={"chat_id": 12345, "text": "service started"},
        )
