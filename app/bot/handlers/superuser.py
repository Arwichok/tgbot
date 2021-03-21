from aiogram import Dispatcher
from aiogram.types import Message


async def superuser_help(msg: Message):
    await msg.answer(
        "/ping Pong\n"
        "/help Show this page\n"
        "<b>Superuser commands:</b>\n"
        ".superuser (id) create superuser by id\n"
        ".restrict (id)"
    )


async def create_superuser(msg: Message):
    pass


async def not_superuser(msg: Message):
    await msg.answer("You are not Superuser")


def setup(dp: Dispatcher):
    dp.register_message_handler(superuser_help, commands=["help"], is_superuser=1)
    dp.register_message_handler(
        create_superuser, commands=["superuser"], commands_prefix=".", is_superuser=1
    )
