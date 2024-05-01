import typing
import aiohttp
import asyncio




class AioClientSession(object):
    """A wrapper class for aiohttp.ClientSession.

    This class provides a convenient way to manage an aiohttp.ClientSession
    by encapsulating its creation, usage, and cleanup.

    Args:
        object (type): The base class for this class.

    Attributes:
        session (aiohttp.ClientSession): The aiohttp.ClientSession instance.

    """

    def __init__(self):
        self.session: aiohttp.ClientSession = aiohttp.ClientSession()

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, exc_type, exc, tb):
        if not self.session.closed:
            await self.session.close()

    async def close(self):
        if not self.session.closed:
            await self.session.close()

    async def request(self, method: str, url: str, should_read=False, **kwargs):
        """Send an HTTP request.

        Args:
            method (str): The HTTP method to use (e.g., 'GET', 'POST').
            url (str): The URL to send the request to.
            should_read (bool, optional): Whether to read the response content. Defaults to False. If false, the session will be closed after the request is made
            **kwargs: Additional keyword arguments to pass to aiohttp.ClientSession.request().

        Returns:
            aiohttp.ClientResponse: The response object.

        """
        async with self.session.request(method, url, **kwargs) as response:
            if should_read:
                await response.read()
            return response

    async def get(self, url: str, should_read=False, **kwargs):
        """Send a GET request.

        Args:
            url (str): The URL to send the request to.
            should_read (bool, optional): Whether to read the response content. Defaults to False.
            **kwargs: Additional keyword arguments to pass to aiohttp.ClientSession.request().

        Returns:
            aiohttp.ClientResponse: The response object.

        """
        return await self.request('GET', url, should_read, **kwargs)

    async def post(self, url: str, should_read=False, **kwargs):
        """Send a POST request.

        Args:
            url (str): The URL to send the request to.
            should_read (bool, optional): Whether to read the response content. Defaults to False.
            **kwargs: Additional keyword arguments to pass to aiohttp.ClientSession.request().

        Returns:
            aiohttp.ClientResponse: The response object.

        """
        return await self.request('POST', url, should_read, **kwargs)

    async def multi_request(self, method: typing.Callable, urls: typing.List[str], should_read=False, **kwargs):
        """Send multiple requests concurrently.

        Args:
            method (Callable): The request method to use (e.g., self.get, self.post).
            urls (List[str]): The URLs to send the requests to.
            should_read (bool, optional): Whether to read the response content. Defaults to False.
            **kwargs: Additional keyword arguments to pass to the request method.

        Returns:
            List[aiohttp.ClientResponse]: The list of response objects.

        """
        return await asyncio.gather(*[method(url, should_read, **kwargs) for url in urls])
    


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