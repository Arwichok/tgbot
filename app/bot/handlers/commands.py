import logging
import time

from aiogram import Dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message
from asyncpg import Connection

from ...models.user import create_user
from ...utils import funcs

logger = logging.getLogger(__name__)


async def start(msg: Message, db: Connection):
    await msg.answer("Hello my dear friend!")
    logger.info(f"{msg.from_user.first_name} {msg.text}")
    await create_user(db, msg.from_user.id)


async def ping(msg: Message):
    start: float = time.time()
    pong_msg: Message = await msg.answer("pong")
    delta: int = funcs.delta_time(start)
    await pong_msg.edit_text(f"{delta}ms")
    logger.info(f"{msg.from_user.first_name}:{msg.text} -> {delta}ms")


def setup(dp: Dispatcher):
    dp.register_message_handler(start, CommandStart())
    dp.register_message_handler(ping, commands=["ping"])
