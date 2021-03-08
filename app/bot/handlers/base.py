import time

from aiogram.dispatcher.filters.builtin import CommandStart

from ...utils import funcs


async def cmd_start(msg, db, log):
    res = await db.fetchval("SELECT 1")
    await msg.answer(f"Hello my dear friend! db: {res}")
    log.append(f"msg | {msg.from_user.first_name} : {msg.text}")


async def cmd_ping(msg):
    start = time.time()
    pong_msg = await msg.answer("pong")
    delta = funcs.delta_time(start)
    await pong_msg.edit_text(f"{delta}ms")


def setup_handlers(dp):
    dp.register_message_handler(cmd_start, CommandStart())
    dp.register_message_handler(cmd_ping, commands=["ping"])
