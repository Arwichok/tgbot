from aiogram import Bot, Dispatcher

from ..models.base import init_db
from ..utils import config
from .handlers.base import setup_handlers
from .middlewares.db import DBMiddleware
from .middlewares.log import LogMiddleware


async def on_startup(dp):
    setup_handlers(dp)
    db_pool = await init_db()
    dp.middleware.setup(DBMiddleware(db_pool))
    dp.middleware.setup(LogMiddleware())


async def on_shutdown(dp):
    pass


def init_dp():
    bot = Bot(config.TG_BOT_TOKEN)
    dp = Dispatcher(bot)
    Bot.set_current(bot)
    Dispatcher.set_current(dp)
    return dp
