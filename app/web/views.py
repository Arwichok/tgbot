from aiohttp import web


async def index(request: web.Request):
    return web.Response(text="H3llo us3r")
