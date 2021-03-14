import logging
import time

from aiogram import Dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message
from asyncpg import Connection

from ...models import user
from ...utils import funcs

logger = logging.getLogger(__name__)


async def start(msg: Message, db: Connection):
    tg_user: int = msg.from_user
    await user.create_user(db, tg_user.id)
    await msg.answer("Hello my dear friend!")
    logger.info(f"{tg_user.first_name} {msg.text}")


async def ping(msg: Message):
    start: float = time.time()
    pong_msg: Message = await msg.answer("pong")
    delta: int = funcs.delta_time(start)
    await pong_msg.edit_text(f"{delta}ms")
    logger.info(f"{msg.from_user.first_name}:{msg.text} -> {delta}ms")


def setup(dp: Dispatcher):
    dp.register_message_handler(start, CommandStart())
    dp.register_message_handler(ping, commands=["ping"])
