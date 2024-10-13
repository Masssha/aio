import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8080/user') as response:
            print(response.status)

asyncio.run(main())