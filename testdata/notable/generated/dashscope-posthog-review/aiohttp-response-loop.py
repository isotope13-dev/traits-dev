import aiohttp

async def read_parts(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            reader = aiohttp.MultipartReader.from_response(response)
            parts = []
            while True:
                part = await reader.next()
                if part is None:
                    break
                parts.append(await part.read())
            return parts
