import logging
import asyncpg

from aiogram import Bot, Dispatcher

from ..models.base import init_db
from .handlers.base import setup_handlers
#from .middlewares impor DBMiddleware
from ..utils import config



async def on_startup(dp):
    setup_handlers(dp)
    db_pool = await init_db()
    logging.info('Startup bot')
    ... # dp.middleware.setup(DBMiddleware(pool))


async def on_shutdown(dp):
    logging.info('Shutdown')




def init_dp():
    bot = Bot(config.TG_BOT_TOKEN)
    dp = Dispatcher(bot)
    Bot.set_current(bot)
    Dispatcher.set_current(dp)
    return dp
