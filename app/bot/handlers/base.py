import logging

from aiogram.dispatcher.filters.builtin import CommandStart


async def cmd_start(msg):
    await msg.answer("Hello my dear friend!")
    logging.info(f"msg | {msg.from_user.first_name} : {msg.text}")


def setup_handlers(dp):
    dp.register_message_handler(cmd_start, CommandStart())
