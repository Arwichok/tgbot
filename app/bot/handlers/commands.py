import logging
import time

from aiogram import Dispatcher
from aiogram.dispatcher.filters.builtin import CommandHelp, CommandStart
from aiogram.types import Message
from asyncpg import Connection

from ...models.user import User
from ...utils import funcs

logger = logging.getLogger(__name__)


async def start(msg: Message, db: Connection):
    tg_user = msg.from_user
    await User.start(db, tg_user.id)
    await msg.answer("Hello my dear friend!")
    logger.info(f"{tg_user.first_name} {msg.text}")


async def ping(msg: Message):
    start: float = time.time()
    pong_msg: Message = await msg.answer("pong")
    delta: int = funcs.delta_time(start)
    await pong_msg.edit_text(f"{delta}ms")
    logger.info(f"{msg.from_user.first_name} /ping -> {delta}ms")


async def help_cmd(msg: Message):
    await msg.answer("/ping Pong\n" "/help Show this page")


def setup(dp: Dispatcher):
    dp.register_message_handler(start, CommandStart())
    dp.register_message_handler(ping, commands=["ping"])
    dp.register_message_handler(help_cmd, CommandHelp())
