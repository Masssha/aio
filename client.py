import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:8080/user/',
                                json={'name': 'rrddttt'}) as response:
            print(response.status)
            print(await response.text())

    async with session.get('http://127.0.0.1:8080/user/5/') as response:
            print(response.status)
            print(await response.text())

    async with session.post('http://127.0.0.1:8080/user/',
                        json={'name': 'Marie'}) as response:
            print(response.status)
            print(await response.text())

    async with session.post('http://127.0.0.1:8080/post/',
                        json={'owner_name': 'rrddttt', 'owner_id': 1, 'title': 'dogs', 'description': 'why do they like cats'}):
            print(response.status)
            print(await response.text())

    async with session.post('http://127.0.0.1:8080/post/',
                        json={'owner_name': 'Marie', 'owner_id': 2, 'title': 'dogs', 'description': 'why do they like cats'}):
            print(response.status)
            print(await response.text())

    async with session.patch('http://127.0.0.1:8080/post/2/',
                        json={'owner_name': 'Marie', 'owner_id': 2, 'title': 'dogs', 'description': 'why they do not like cats'}):
            print(response.status)
            print(await response.text())

    async with session.get('http://127.0.0.1:8080/post/1/'):
            print(response.status)
            print(await response.text())

    async with session.delete('http://127.0.0.1:8080/post/1/'):
            print(response.status)
            print(await response.text())



asyncio.run(main())