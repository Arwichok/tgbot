from aiogram import Bot, Dispatcher
from aiogram.dispatcher.storage import BaseStorage
from aiogram.types import BotCommand, ParseMode
from asyncpg.pool import Pool

from ..models.base import init_db, setup_models
from ..utils import config
from .filters.base import setup_filters
from .handlers.base import setup_handlers
from .middlewares.base import setup_middlewares
from .states.storage import init_storage


async def on_startup(dp: Dispatcher, pool: Pool):
    await pool
    await set_my_commands(dp)
    await setup_models(pool)
    setup_middlewares(dp, pool)
    setup_filters(dp)
    setup_handlers(dp)


async def on_shutdown(dp: Dispatcher):
    pass


def init_dp(token: str=config.TG_BOT_TOKEN) -> Dispatcher:
    bot = Bot(
        token=token,
        parse_mode=ParseMode.HTML,
        proxy=config.PROXY_URL,
        proxy_auth=config.PROXY_AUTH,
    )
    storage: BaseStorage = init_storage()
    dp = Dispatcher(bot, storage=storage)
    Bot.set_current(bot)
    Dispatcher.set_current(dp)
    return dp


async def set_my_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            BotCommand("/start", "🟢 Setup bot"),
            BotCommand("/ping", "🏓 Pong"),
            BotCommand("/help", "Help page"),
        ]
    )
