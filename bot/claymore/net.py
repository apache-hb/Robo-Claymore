from aiohttp import ClientSession

async def json_request(url: str):
    async with ClientSession() as session:
        async with session.get(url) as res:
            return await res.json()
