import asyncio
import logging

import aiohttp

from .. import bot, web, models
from . import config


logging.basicConfig(
    level=logging.INFO,
    format=config.LOG_FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S %z")



async def web_app():
    '''
        Initialise and return webapp
    '''
    _app = aiohttp.web.Application()
    _app['pool'] = await models.base.create_pool()
    await web.routes.setup(_app)
    await bot.webhook.setup(_app)
    return _app


def webhook():
    aiohttp.web.run_app(
        web_app(),
        host=config.LC_HOST,
        port=config.LC_PORT
    )


def cli():
    webhook()





