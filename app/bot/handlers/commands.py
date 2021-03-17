import logging
import time

from aiogram import Dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message
from aiogram.utils import markdown as md
from asyncpg import Connection

from ...models.user import User
from ...utils import funcs

logger = logging.getLogger(__name__)


async def start(msg: Message, db: Connection, db_user):
    tg_user = msg.from_user
    await User.start_conversation(db, tg_user.id)
    await msg.answer("Hello my dear friend!")
    logger.info(f"{tg_user.first_name} {msg.text}")


async def ping(msg: Message):
    start: float = time.time()
    pong_msg: Message = await msg.answer("pong")
    delta: int = funcs.delta_time(start)
    await pong_msg.edit_text(f"{delta}ms")
    logger.info(f"{msg.from_user.first_name} {msg.text} -> {delta}ms")


async def superuser(msg: Message):
    await msg.answer(md.hbold("Hello Superuser"))


async def not_superuser(msg: Message):
    await msg.answer(md.hbold("You are not Superuser"))


def setup(dp: Dispatcher):
    dp.register_message_handler(start, CommandStart())
    dp.register_message_handler(ping, commands=["ping"])
    dp.register_message_handler(superuser, commands=["admin"], is_superuser=1)
    dp.register_message_handler(not_superuser, commands=["admin"])
