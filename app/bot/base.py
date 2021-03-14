import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, ParseMode
from asyncpg.pool import Pool

from ..models.base import init_db
from ..utils import config
from .handlers.base import setup_handlers
from .middlewares.db import DBMiddleware
from .middlewares.log import LogMiddleware


async def on_startup(dp: Dispatcher):
    setup_handlers(dp)
    db_pool: Pool = await init_db()
    dp.middleware.setup(DBMiddleware(db_pool))
    dp.middleware.setup(LogMiddleware())
    await set_my_commands(dp)
    logging.info("\033[1;34mBotStarted\033[0m")


async def on_shutdown(dp: Dispatcher):
    pass


def init_dp() -> Dispatcher:
    bot = Bot(
        token=config.TG_BOT_TOKEN,
        parse_mode=ParseMode.HTML,
        proxy=config.PROXY_URL,
        proxy_auth=config.PROXY_AUTH)
    dp = Dispatcher(bot)
    Bot.set_current(bot)
    Dispatcher.set_current(dp)
    return dp


async def set_my_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [BotCommand("/start", "🟢 Setup bot"), BotCommand("/ping", "🏓 Pong")]
    )
