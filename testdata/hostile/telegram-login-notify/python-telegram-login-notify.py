import aiohttp


async def notify_panel(app):
    login_url = f"http://{app['host']}:{app['port']}/{app['panel_route']}/login"
    async with aiohttp.ClientSession() as session:
        await session.get(
            "https://api.telegram.org/bot123456789012:AbCdEf1234567890AbCdEf1234567890/sendMessage",
            params={"chat_id": 12345, "text": login_url},
        )
