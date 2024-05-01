# aiohttp_wrapper
 A python wrapper for aiohttp to make it easier to reuse sessions


### There are 2 ways you can use this class
<li>With the async with context manager</li>
<li>Without the `async with` context manager </li>

```py

async def with_context_manager(url:str):
    async with AioClientSession() as session:
        response = await session.get(url, should_read=True)
        print(await response.text())



async def without_context_manager(url:str):
    session = AioClientSession()
    try:
        response = await session.get(url, should_read=True)
        print(await response.text())
    except Exception as e:
        # handle exception
        print(e)
    finally:
        await session.close()



asyncio.run(without_context_manager('https://nekos.life/api/v2/img/neko'))
```