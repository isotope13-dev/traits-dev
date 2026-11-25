import aiohttp, asyncio

async def check_exposed(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{url}/core/install.php") as resp:
            text = await resp.text()
            if "Database configuration" in text:
                print("Installer exposed!")

DEFAULT_CFG = {
    "driver": "sqlite",
    "database": "sites/default/files/.ht.sqlite",
    "site_name": "My Drupal Site",
}
