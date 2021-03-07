import logging
import asyncpg

from aiogram import Bot, Dispatcher

from .. import models
from .handlers.base import setup_handlers
#from .middlewares impor DBMiddleware
from ..utils import config


def setup(dp):
    setup_handlers(dp)


async def on_startup(dp):
    setup_handlers(dp)
    ... # dp.middleware.setup(DBMiddleware(pool))


async def on_shutdown(dp):
    logging.info('Shutdown')




def init_dp():
	bot = Bot(config.TG_BOT_TOKEN)
	dp = Dispatcher(bot)
	return dp
