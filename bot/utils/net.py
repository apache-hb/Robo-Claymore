import aiohttp

HEADERS = {
    'User-Agent': 'RoboClaymore (by ApacheActual#6945 on discord)'
}

async def json(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers = HEADERS) as resp:
            return await resp.json()
