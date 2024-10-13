import aiohttp
import asyncio

# async def main():
#     async with aiohttp.ClientSession() as session:
#         async with session.get('http://127.0.0.1:8080/user') as response:
#             print(response.status)
#
# asyncio.run(main())

# response = requests.post('http://127.0.0.1:8081/user/',
#                         json={'name': 'rrddttt'})

# response = requests.get('http://127.0.0.1:8081/user/5/')

# response = requests.post('http://127.0.0.1:8081/user/',
#                         json={'name': 'Marie'})

# response = requests.post('http://127.0.0.1:8081/post/',
#                         json={'owner_name': 'rrddttt', 'owner_id': 1, 'title': 'dogs', 'description': 'why do they like cats'})

# response = requests.post('http://127.0.0.1:8081/post/',
#                         json={'owner_name': 'Marie', 'owner_id': 2, 'title': 'dogs', 'description': 'why do they like cats'})

# response = requests.patch('http://127.0.0.1:8081/post/2/',
#                         json={'owner_name': 'Marie', 'owner_id': 2, 'title': 'dogs', 'description': 'why they do not like cats'})


response = requests.post('http://127.0.0.1:8081/post/',
                        json={'owner_name': 'Marie', 'owner_id': 2, 'title': 'hehe', 'description': 'shit'})

# response = requests.get('http://127.0.0.1:8081/post/1/')

# response = requests.delete('http://127.0.0.1:8081/post/1/')

print(response.status_code)
print(response.text)