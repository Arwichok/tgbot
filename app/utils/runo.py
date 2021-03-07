import logging

import aiohttp
import asyncpg

from ..models.base import init_db
from ..bot.webhook import setup_bot
from ..web.routes import setup_routes
from . import config



def run():
    aiohttp.web.run_app(init_app(), **config.APP_CONFIG)


async def init_app():
    app = aiohttp.web.Application()

    db_pool = await init_db()

    setup_bot(app)
    setup_routes(app)

    return app


logging.basicConfig(
        level=logging.INFO,
        format=config.LOG_FORMAT,
        datefmt="%Y-%m-%d %H:%M:%S %z")
