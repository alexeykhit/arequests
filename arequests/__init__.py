import json

from aiohttp import ClientSession, ClientResponse

__version__ = '0.1.2'


class Response:
    def __init__(self, response: ClientResponse, content):
        self.content = content
        self.response = response

    @property
    def headers(self):
        return self.response.headers

    @property
    def status_code(self):
        return self.response.status

    @property
    def text(self):
        encoding = self.response.get_encoding()
        return self.content.decode(encoding, errors='strict')

    def json(self):
        return json.loads(self.text)


class Session:
    def __init__(self):
        self.session = ClientSession()
        self.headers = None
        self.params = None

    async def close(self):
        await self.session.close()

    async def request(self, method, url, **kwargs) -> Response:
        if self.headers:
            kwargs.setdefault('headers', {}).update(self.headers)
        if self.params:
            kwargs.setdefault('params', {}).update(self.params)

        async with self.session.request(method, url, **kwargs) as r:
            content = await r.read()
            return Response(r, content)

    async def get(self, url, **kwargs) -> Response:
        return await self.request('GET', url, **kwargs)

    async def post(self, url, **kwargs) -> Response:
        return await self.request('POST', url, **kwargs)


async def request(method, url, **kwargs) -> Response:
    async with ClientSession() as session:
        async with session.request(method, url, **kwargs) as r:
            content = await r.read()
            return Response(r, content)


async def get(url, **kwargs) -> Response:
    return await request('GET', url, **kwargs)


async def post(url, **kwargs) -> Response:
    return await request('POST', url, **kwargs)
